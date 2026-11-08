# Al-Shifa Modern Hospital (Django)
python -m venv venv && venv\Scripts\activate   (Windows)  |  source venv/bin/activate (Mac/Linux)
pip install Django          (add psycopg2-binary only for PostgreSQL)
python manage.py makemigrations hospital && python manage.py migrate
python manage.py seed && python manage.py createsuperuser
python manage.py runserver     ->  http://127.0.0.1:8001
PostgreSQL: set DB_NAME, DB_USER, DB_PASSWORD, DB_HOST; production: DEBUG=0, SECRET_KEY=...
