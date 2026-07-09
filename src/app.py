"""Dashboard interativo (Shiny for Python).

Vistas disponíveis:
  1. Evolução do total faturado por mês (com seletor de intervalo temporal).
  2. Comparação de clientes / análise de um cliente individual.
  3. Funcionalidade própria — "Alertas de Validação": resumo, por ficheiro,
     dos NIF/NIB que falham a validação (Anexos A e B do enunciado), para dar
     visibilidade imediata à qualidade dos dados recebidos.

Executar (a partir da raiz do projeto)::

    shiny run --reload src/app.py

Docs: https://shiny.posit.co/py/
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd
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
ALERTAS = ag.resumo_alertas(FICHEIROS)
TOTAL_NIBS_INVALIDOS = sum(a["n_nibs_invalidos"] for a in ALERTAS)


# interface do dashboard: sidebar de filtros + value_boxes + graficos + tabela
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
        ui.value_box("NIBs inválidos detetados", ui.output_text("n_nibs_invalidos")),
    ),
    ui.card(ui.card_header("Evolução mensal do total faturado"),
            output_widget("grafico_mensal")),
    ui.layout_columns(
        ui.card(ui.card_header("Total por cliente (período completo)"),
                output_widget("grafico_clientes")),
        ui.card(ui.card_header("Cliente selecionado — evolução mensal"),
                output_widget("grafico_cliente")),
    ),
    ui.card(
        ui.card_header("Alertas de Validação (funcionalidade própria) — NIF/NIB por ficheiro"),
        ui.output_data_frame("tabela_alertas"),
    ),
    title="Dashboard Débitos Diretos — IPCA Energy",
)


def server(input, output, session):
    """Liga os \"inputs\" da UI (filtros) aos \"outputs\" (texto, gráficos, tabela).

    Todos os cálculos partem dos dados carregados uma única vez ao arrancar
    a app (:data:`FICHEIROS`, :data:`ALERTAS`, etc.); as funções abaixo são
    reativas ao estado dos filtros (:func:`meses_no_intervalo`, seleção de
    cliente).
    """

    @reactive.calc
    def meses_no_intervalo() -> list[str]:
        """Lista de períodos AAAA-MM entre os filtros de mês inicial/final."""
        ini, fim = input.mes_ini(), input.mes_fim()
        return [m for m in MESES if ini <= m <= fim]

    @render.text
    def n_ficheiros():
        """Nº total de ficheiros PS2 carregados de ``data/``."""
        return str(len(FICHEIROS))

    @render.text
    def total_periodo():
        """Total faturado (€), somado apenas nos meses do intervalo selecionado."""
        tot = ag.total_por_mes(FICHEIROS)
        return f"{sum(v for m, v in tot.items() if m in meses_no_intervalo()):,.2f}"

    @render.text
    def n_avisos():
        """Nº de ficheiros que falharam a validação de estrutura."""
        return str(len(AVISOS))

    @render.text
    def n_nibs_invalidos():
        """Nº total de NIBs de cliente inválidos, em todos os ficheiros."""
        return str(TOTAL_NIBS_INVALIDOS)

    @render.data_frame
    def tabela_alertas():
        """Tabela de Alertas de Validação (funcionalidade própria), filtrada por período."""
        meses = set(meses_no_intervalo())
        linhas = [a for a in ALERTAS if a["periodo"] in meses]
        df = pd.DataFrame(linhas).rename(columns={
            "periodo": "Período",
            "nif": "NIF ordenante",
            "nif_valido": "NIF válido",
            "n_movimentos": "Nº movimentos",
            "n_nibs_invalidos": "NIBs inválidos",
        })
        return render.DataGrid(df, filters=True)

    @render_plotly
    def grafico_mensal():
        """Gráfico de linha: total faturado por mês, no intervalo selecionado."""
        tot = ag.total_por_mes(FICHEIROS)
        meses = meses_no_intervalo()
        fig = px.line(x=meses, y=[tot[m] for m in meses], markers=True,
                      labels={"x": "Mês", "y": "Total (€)"})
        return fig

    @render_plotly
    def grafico_clientes():
        """Gráfico de barras: total faturado por cliente (NIB), período completo."""
        tot = ag.total_por_cliente(FICHEIROS)
        # NIB abreviado para leitura
        nibs = list(tot.keys())
        fig = px.bar(x=[n[:8] + "…" for n in nibs], y=list(tot.values()),
                     labels={"x": "Cliente (NIB)", "y": "Total (€)"})
        return fig

    @render_plotly
    def grafico_cliente():
        """Gráfico de barras: evolução mensal do cliente (NIB) selecionado."""
        serie = ag.serie_cliente(FICHEIROS, input.nib())
        meses = [m for m in serie if m in meses_no_intervalo()]
        fig = px.bar(x=meses, y=[serie[m] for m in meses],
                     labels={"x": "Mês", "y": "Faturado (€)"})
        return fig


app = App(app_ui, server)
