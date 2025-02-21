# Simplestock

Simplestock is an online store that promotes the idea of simplicity and a user-accessible interface that is easy to use. It contains only the essential features, ensuring users can navigate the website quickly and efficiently.

## Disclaimer

🚨 **WARNING!** This project does not intend to violate any copyright claims.  
It has been created for **educational purposes only**.

## Tech Stack

- **Backend:** Python, Django, FastAPI, SQLite3  
- **Frontend:** HTML, CSS, JavaScript  

## Project Status

This project is still in progress.

## Installation and Setup

Follow these steps to run Simplestock on your local machine:

1. Install dependencies:  
   ```pip install -r "requirements.txt"```

2. Apply migrations:  
   ```python manage.py makemigrations; python manage.py migrate```  
   After running migrations, modify the database:  
   In the `cities-light` tables, delete all entries where `country_id != 38`

3. Run the project using one of the following methods:

   - **Method 1 (Django & FastAPI separately):**  
     ```python manage.py runserver```  
     ```uvicorn backend_fastapi:app --reload --port 8080```  

   - **Method 2 (Using Docker):**  
     ```cd docker```  
     ```docker-compose up --build```
