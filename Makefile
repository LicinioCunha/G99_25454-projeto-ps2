.PHONY: venv install test validate dashboard relatorio clean

VENV := .venv
PY := $(VENV)/Scripts/python.exe

venv:
	python -m venv $(VENV)

install: venv
	$(PY) -m pip install -r requirements.txt

test:
	$(PY) -m pytest -v

validate:
	$(PY) src/main.py

dashboard:
	$(PY) -m shiny run --reload src/app.py

relatorio:
	cd docs/relatorio && latexmk -pdf main.tex

clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +
	rm -rf .pytest_cache
	cd docs/relatorio && latexmk -c
