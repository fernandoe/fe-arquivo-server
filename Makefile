install:
	pip install -r requirements.txt

test:
	cd ./source && python manage.py test
