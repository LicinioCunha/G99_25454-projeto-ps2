# Trabalho Prático — Débitos Diretos (formato PS2)

**Laboratórios de Informática** · LESI / LESIPL · 2025/26
**Grupo 99** — Licínio Cunha (nº 25454) — trabalho individual

Dashboard interativo (Python + [Shiny](https://shiny.posit.co/py/)) para análise
de ficheiros de débitos diretos no formato PS2 (versão simplificada).

---

## Como executar

```bash
# 1. criar e ativar ambiente virtual
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. instalar dependências
pip install -r requirements.txt

# 3. validar os ficheiros de dados
python src/main.py

# 4. abrir o dashboard
shiny run --reload src/app.py
# depois abrir http://127.0.0.1:8000 no browser
```

No VS Code há duas configurações prontas em `.vscode/launch.json`
("Validar ficheiros" e "Dashboard Shiny") — basta usar o painel _Run and Debug_.

## Estrutura do projeto

```
projeto-ps2/
├── data/                # ficheiros DD_AAAA_MM.ps2
├── src/
│   ├── ps2/
│   │   ├── leitura.py     # listar/ler ficheiros (ETAPAS 1-2)
│   │   ├── modelo.py      # objetos de domínio (dataclasses)
│   │   ├── parsing.py     # extração de campos por slicing (ETAPA 3)
│   │   ├── validacao.py   # estrutura + NIF + NIB (ETAPA 4)
│   │   ├── agregacao.py   # totais por mês/cliente (ETAPA 6)
│   │   └── carregador.py  # leitura + parsing de alto nível
│   ├── main.py           # relatório de validação (CLI)
│   └── app.py            # dashboard Shiny
├── docs/relatorio/      # relatório em LaTeX
├── requirements.txt
└── README.md
```

## Formato PS2 (simplificado) — posições confirmadas

| Registo | Campo | Posição (base 1) |
|---|---|---|
| Cabeçalho (1) | data AAAAMMDD | 2–9 |
| | empresa | 10–52 |
| | NIF | 53–61 |
| | total (cêntimos) | 62–75 |
| | nº registos | 76–81 |
| Movimento (2) | referência/ADC | 2–11 |
| | NIB (21 díg) | 12–32 |
| | importância (cêntimos) | 42–55 |
| | descrição | 56–82 |
| Fim (9) | total (cêntimos) | 2–15 |
| | nº registos | 16–21 |

> **Nota sobre validação de NIB:** a regra do Anexo B (`int(nib) % 97 == 1`)
> marca todos os NIBs dos dados como inválidos — o próprio exemplo do enunciado
> dá 96, não 1. A confirmar com o docente.

## Estratégia de trabalho no Git

Trabalho individual — sem divisão de tarefas por elementos de grupo.

| Elemento | Nº | Branch | Período |
|---|---|---|---|
| Licínio Cunha | 25454 | `feature-leitura` | 20/06 a 09/07/2026 |

## Funcionalidade própria do grupo

_Descrever aqui a funcionalidade extra escolhida (ver `src/app.py`, secção TODO)._

## Conclusão

_A escrever no fim do trabalho._
