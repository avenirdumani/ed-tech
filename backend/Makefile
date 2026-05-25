run-server:
	python -m	uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload

run-seed:
	python -m scripts.seed

run-tests:
	python -m pytest --cov=src tests/* --cov-report html -s
