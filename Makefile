migrate:
	which python
	python manage.py makemigrations members
	python manage.py migrate

.phony: migrate