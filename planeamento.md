# Trabalho Prático

**Laboratórios de Informática**

Licenciatura em Engenharia de Sistemas Informáticos (*regime pós-laboral*) 2025-26

## grupo  *99*

Trabalho realizado individualmente.

| #      | Número  | Nome |
| -----  | -----   | ---- |
| _A1_   | 25454   | Licínio Cunha  |


## Planeamento

### Semana 1 - [20.jun a 26.jun]

> leitura de ficheiros .ps2 na pasta `./data`
> validar se conteúdo do ficheiro respeita a formatação ps2
> validar nifs e NIBs (seguem as regras)

| #      | Branch            | Descrição da Tarefa |
| -----  | -----------       | ---- |
| _A1_   | feature-leitura   | Leitura/listagem de ficheiros (`ps2/leitura.py`), modelo de domínio (`ps2/modelo.py`) e parsing por slicing (`ps2/parsing.py`) confirmando as posições dos campos com os ficheiros de exemplo.  |

### observações / decisões

Licínio Cunha (nº 25454, A1): trabalho realizado entre 20 de junho e 9 de julho de 2026.



## Semana 2 - [27.jun a 03.jul]

| #      | Branch  | Descrição da Tarefa |
| -----  | -----   | ---- |
| _A1_   | feature-validacao | Validação de estrutura (ordem dos registos, totais, contagens) e validação de NIF/NIB (Anexos A e B) em `ps2/validacao.py`; `src/main.py` como CLI de relatório. |

### observações / decisões

Confirmado que os exemplos dos Anexos A e B do próprio enunciado não
verificam o algoritmo descrito (NIF `501845923` e NIB
`003506510000258741254`) — implementadas as regras tal como documentadas,
questão assinalada no README para confirmação com o docente.


## Semana 3 - [04.jul a 06.jul]

| #      | Branch  | Descrição da Tarefa |
| -----  | -----   | ---- |
| _A1_   | feature-dashboard | Agregações (`ps2/agregacao.py`: total por mês, por cliente, série de cliente) e primeira versão do dashboard Shiny (`src/app.py`) com filtro de período e seleção de cliente. |

### observações / decisões

Estrutura do projeto organizada em pacote `ps2/` com um ficheiro por
responsabilidade, para facilitar testes unitários.


## Semana 4 - [07.jul a 08.jul]

| #      | Branch  | Descrição da Tarefa |
| -----  | -----   | ---- |
| _A1_   | feature-alertas-validacao | Funcionalidade própria: vista "Alertas de Validação" no dashboard (`resumo_alertas`), expansão da suite de testes (parsing, agregação, estrutura, NIB, integração com `data/`) e correção do encoding da consola no Windows. |
| _A1_   | feature-readme | Inicialização do repositório Git, README (testes, funcionalidade própria, estratégia de git, conclusão) e relatório em LaTeX. |

### observações / decisões

Repositório Git inicializado só nesta fase (era o maior risco em falta);
passou a seguir-se estritamente o fluxo branch → *pull request* → `main`,
sem eliminar branches após integração.


## Semana 5 - [09.jul]

> testes de integração finais
> preparar versão final do relatório

| #      | Branch  | Descrição da Tarefa |
| -----  | -----   | ---- |
| _A1_   | feature-relatorio | Revisão final dos testes (`pytest`), fecho do relatório LaTeX e criação da *release* no GitHub. |

### observações / decisões


