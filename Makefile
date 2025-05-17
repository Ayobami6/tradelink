.PHONY: run
run:
	@python manage.py runserver $(port)

install:
	@pip install $(package)

csu:
	@python manage.py createsuperuser

mms:
	@python manage.py makemigrations

migrate:
	@python manage.py migrate

shell:
	@python manage.py shell

dbshell:
	@python manage.py dbshell

celery:
	@celery -A tradelink worker -l info

celery-beat:
	@celery -A tradelink beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

test:
	@pytest