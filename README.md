# MovieScreen

basic django website for first time learners

For documentation: https://docs.djangoproject.com/en/5.0/

Prerequisite install python. To see which version visit https://docs.djangoproject.com/en/5.0/faq/install/#what-python-version-can-i-use-with-django

How to make virtual environment?

In linux env
1. python3 -m venv myvenv
source myvenv/bin/activate

2. pip install -r requirements.txt

deactivate

before coding you need to install django in ypur virtual env:

pip install django

if you made changed in your models do:

python manage.py makemigrations

python manage.py migrate

to run the server do:
python manage.py runserver

installed a new package?
pip freeze > requirements.txt
