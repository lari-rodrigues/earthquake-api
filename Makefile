install:
	pip3 install -r requirements.txt

venv:
	python3 --version && python3 -m venv venv

unit-tests:
	python3 -m pytest src/tests/unit/

execute:
	uvicorn src.app:app