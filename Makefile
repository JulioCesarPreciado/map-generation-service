# Punto de entrada del microservicio
RUN=uvicorn app.main:app --reload

# Variables
PYTHON=python
PIP=pip

# Comandos
install:
	$(PIP) install -r requirements.txt

run:
	$(RUN)

test:
	PYTHONPATH=. pytest

lint:
	flake8 app tests

format:
	black app tests

freeze:
	$(PIP) freeze > requirements.txt

docs:
	cd docs && make html