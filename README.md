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

# 4. correr os testes
pytest

# 5. abrir o dashboard
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
├── tests/               # testes unitários e de integração (pytest)
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
> marca todos os NIBs dos dados (e o próprio exemplo do Anexo B, que dá 96 em
> vez de 1) como inválidos. A regra foi implementada literalmente como está
> descrita no enunciado (ver `tests/test_validacao.py::test_valida_nib_exemplo_anexo_b`);
> fica a aguardar confirmação do docente se o algoritmo pretendido é outro.

## Testes

O projeto tem testes unitários (parsing, validação de NIF/NIB, validação de
estrutura, agregações) e um teste de integração que carrega toda a pasta
`data/`. Correr com:

```bash
pytest -v
```

## Funcionalidade própria

**Alertas de Validação**: uma vista no dashboard (tabela + contador) que
resume, ficheiro a ficheiro, quantos NIF/NIB falham a validação dos Anexos A
e B. A validação de estrutura já garante que os totais e o nº de registos
batem certo; esta vista dá visibilidade imediata à qualidade dos dados
(NIF do ordenante e NIBs de cliente) diretamente no dashboard, sem ser preciso
consultar a consola (`src/main.py`). Implementada em `ps2/agregacao.py`
(`resumo_alertas`) e exposta em `src/app.py` (`tabela_alertas`).

## Estratégia de trabalho no Git

Trabalho individual — sem divisão de tarefas por elementos de grupo, mas
seguindo a mesma disciplina de branches + *pull requests* pedida para
trabalho em grupo:

- Uma branch de funcionalidade por tema (ex.: `feature-alertas-validacao`,
  `feature-readme`), nunca commits diretos em `main`.
- Integração em `main` sempre por *pull request* no GitHub (mesmo sendo o
  único contribuidor), para manter o histórico de alterações documentado.
- Branches **não são eliminadas** depois de integradas.
- Mensagens de commit em português, no imperativo, com prefixo semântico
  (`feat:`, `fix:`, `chore:`, `docs:`, `test:`).

| Elemento | Nº | Período |
|---|---|---|
| Licínio Cunha | 25454 | 20/06 a 09/07/2026 |

## Conclusão

O trabalho cobre o ciclo completo pedido no enunciado: leitura dos ficheiros
PS2 da pasta `data/`, validação de estrutura e de NIF/NIB (Anexos A e B),
agregação da informação (por mês e por cliente) e um dashboard interativo em
Shiny com filtro de período, comparação de clientes e a funcionalidade
própria de alertas de validação. A maior dificuldade foi confirmar as
posições exatas dos campos no layout PS2 simplificado (resolvida por
inspeção direta dos ficheiros de exemplo) e perceber que os próprios exemplos
do enunciado (NIF e NIB) não batem certo com o algoritmo descrito — decidiu-se
implementar as regras tal como documentadas e assinalar essa discrepância nos
testes e neste README. Como trabalho futuro, ficam por explorar: exportação
dos alertas para CSV, deteção de meses atípicos por desvio-padrão, e suporte
a IBAN (PT50 + NIB) em vez do NIB isolado.
