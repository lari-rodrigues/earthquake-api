install:
	pip3 install -r src/requirements.txt

venv:
	python3 --version && python3 -m venv venv

unit-tests:
	python3 -m pytest src/tests/unit/

execute:
	uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload