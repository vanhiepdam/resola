lint:
	@echo "Running linter..."
	flake8 . --exclude=venv

	@echo "Running dependencies checker..."
	poetry export -f requirements.txt --output requirements.txt --without-hashes --dev
	safety check --bare -r requirements.txt

	@echo "Running type annotation checking..."
	mypy .


migrations:
	@echo "Running migrations..."
	python src/manage.py makemigrations

migrate:
	python src/manage.py migrate


start:
	@echo "Starting server..."
	python src/manage.py runserver


shell:
	@echo "Starting shell..."
	python src/manage.py shell
