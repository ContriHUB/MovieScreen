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

##    Connecting to the OMDB API
To fetch movie data from OMDB, you need to create an API key. Follow these steps:
1. Go to the OMDB API website: https://www.omdbapi.com
2. Click on the API Key tab.
3. Scroll down to the Pricing section and select the Free or Paid plan depending on your usage.
4. Sign up for an account using your email.
5. Verify your email and log in.
6. Navigate to the API Key section in your profile.
7. Copy your generated API key.

###    Adding the OMDB API Key to Your Project
1. Create a .env file in the root directory of your project:
```bash
touch .env
```
2. Add your OMDB API key to the .env file:
```bash
OMDB_API_KEY=your_api_key_here
```
3. In your Django settings or configuration file, load the API key from the .env file:
 ```bash
import os
from dotenv import load_dotenv

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
```  
4. Use the OMDB_API_KEY in your code when making API requests.


## Contributing 
While raing the pull request, add ypur name to the CONTRIBUTORS.md file

## Updating requirements.txt
While adding packages, update requirements.
```bash
pip freeze > requirements.txt
```
