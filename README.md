# MovieScreen

basic django website for first time learners
For documentation: https://docs.djangoproject.com/en/5.0/
Prerequisite install python. To see which version visit https://docs.djangoproject.com/en/5.0/faq/install/#what-python-version-can-i-use-with-django

How to make virtual environment?
python3 -m venv myvenv

to activate virtual environment:
source myvenv/bin/activate

to deactivate:
deactivate

before coding you need to install django in ypur virtual env:
pip install django

if you made changed in your models do:
python manage.py makemigrations
python manage.py migrate

to run the server do:
python manage.py runserver
