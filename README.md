# MovieScreen

A basic Django website for first-time learners.


## Documentation

For detailed documentation, visit: [Django Documentation](https://docs.djangoproject.com/en/5.0/)

## Prerequisites

- Install Python. To see which version is compatible, visit: [Django FAQ](https://docs.djangoproject.com/en/5.0/faq/install/#what-python-version-can-i-use-with-django)

## Setting Up a Virtual Environment

### On Linux

1. Create a virtual environment:
    ```bash
    python3 -m venv myvenv
    ```

2. Activate the virtual environment:
    ```bash
    source myvenv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Deactivate the virtual environment when done:
    ```bash
    deactivate
    ```

### On Windows

1. Create a virtual environment:
    ```bash
    python -m venv myvenv
    ```

2. Activate the virtual environment:
    ```bash
    myvenv\Scripts\activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Deactivate the virtual environment when done:
    ```bash
    deactivate
    ```
## Running Migrations
Once Django is installed, you need to create the database tables for the application:

Make migrations for your user app:

```bash
   python manage.py makemigrations user
```
Apply the migrations to the database:

```bash
   python manage.py migrate
```
## Installing Django

Before coding, you need to install Django in your virtual environment:
```bash
pip install django
```

## Contributing 
While raing the pull request, add ypur name to the CONTRIBUTORS.md file

## Updating requirements.txt
While adding packages, update requirements.
```bash
pip freeze > requirements.txt
```
## Email config
1. Let most of the email setting as they are.
2. For EMAIL_HOST_USER & DEFAULT_FROM_EMAIL set the mail account you want to send mail from
3. Go to the google manage account for the email you set
    - Enable 2 step verification
    - Generate a HOST_PASSWORD from app password in the gmail account
4. set EMAIL_HOST_PASSWORD to the app password you generated

[Setup Tutorial Refference](https://www.geeksforgeeks.org/setup-sending-email-in-django-project/)

### Note: 
Make sure of the spellcheck.\
Might not work with proxy so try using you cellular network
