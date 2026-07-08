"""Dashboard interativo (Shiny for Python) — ESQUELETO.

Ponto de partida com duas vistas base:
  1. Evolução do total faturado por mês (com seletor de intervalo temporal).
  2. Comparação de clientes / análise de um cliente individual.

>>> TODO (grupo): definir e implementar UMA funcionalidade própria do grupo
    (ver enunciado). Ex.: deteção de meses atípicos, top-N clientes, alertas
    de NIB inválido, exportação, etc.

Executar (a partir da raiz do projeto)::

    shiny run --reload src/app.py

Docs: https://shiny.posit.co/py/
"""
from __future__ import annotations
from pathlib import Path
import plotly.express as px
from shiny import App, reactive, render, ui
from shinywidgets import output_widget, render_plotly

# permitir importar o pacote ps2 quer se corra da raiz quer de src/
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ps2.carregador import carregar_pasta          # noqa: E402
from ps2 import agregacao as ag                     # noqa: E402
from ps2.validacao import valida_nif, valida_nib    # noqa: E402

DATA_DIR = str(Path(__file__).resolve().parent.parent / "data")

# carrega uma vez ao arrancar a app
FICHEIROS, AVISOS = carregar_pasta(DATA_DIR)
MESES = list(ag.total_por_mes(FICHEIROS).keys())
NIBS = ag.clientes(FICHEIROS)


app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h4("Filtros"),
        ui.input_select("mes_ini", "Mês inicial", choices=MESES,
                        selected=MESES[0] if MESES else None),
        ui.input_select("mes_fim", "Mês final", choices=MESES,
                        selected=MESES[-1] if MESES else None),
        ui.hr(),
        ui.input_select("nib", "Cliente (NIB)", choices=NIBS,
                        selected=NIBS[0] if NIBS else None),
    ),
    ui.layout_columns(
        ui.value_box("Ficheiros carregados", ui.output_text("n_ficheiros")),
        ui.value_box("Total no período (€)", ui.output_text("total_periodo")),
        ui.value_box("Avisos de estrutura", ui.output_text("n_avisos")),
    ),
    ui.card(ui.card_header("Evolução mensal do total faturado"),
            output_widget("grafico_mensal")),
    ui.layout_columns(
        ui.card(ui.card_header("Total por cliente (período completo)"),
                output_widget("grafico_clientes")),
        ui.card(ui.card_header("Cliente selecionado — evolução mensal"),
                output_widget("grafico_cliente")),
    ),
    title="Dashboard Débitos Diretos — IPCA Energy",
)


def server(input, output, session):

    @reactive.calc
    def meses_no_intervalo() -> list[str]:
        ini, fim = input.mes_ini(), input.mes_fim()
        return [m for m in MESES if ini <= m <= fim]

    @render.text
    def n_ficheiros():
        return str(len(FICHEIROS))

    @render.text
    def total_periodo():
        tot = ag.total_por_mes(FICHEIROS)
        return f"{sum(v for m, v in tot.items() if m in meses_no_intervalo()):,.2f}"

    @render.text
    def n_avisos():
        return str(len(AVISOS))

    @render_plotly
    def grafico_mensal():
        tot = ag.total_por_mes(FICHEIROS)
        meses = meses_no_intervalo()
        fig = px.line(x=meses, y=[tot[m] for m in meses], markers=True,
                      labels={"x": "Mês", "y": "Total (€)"})
        return fig

    @render_plotly
    def grafico_clientes():
        tot = ag.total_por_cliente(FICHEIROS)
        # NIB abreviado para leitura
        nibs = list(tot.keys())
        fig = px.bar(x=[n[:8] + "…" for n in nibs], y=list(tot.values()),
                     labels={"x": "Cliente (NIB)", "y": "Total (€)"})
        return fig

    @render_plotly
    def grafico_cliente():
        serie = ag.serie_cliente(FICHEIROS, input.nib())
        meses = [m for m in serie if m in meses_no_intervalo()]
        fig = px.bar(x=meses, y=[serie[m] for m in meses],
                     labels={"x": "Mês", "y": "Faturado (€)"})
        return fig


app = App(app_ui, server)
