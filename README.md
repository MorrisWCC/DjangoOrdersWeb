# DjangoOrdersWeb
- Deploy steps:
    - 1. fork and clone this project
    - 2. pip3 install -r requirements.txt
    - 3. python3 manage.py migrate
    - 4. python3 manage.py makemigrations
    - 5. python3 manage.py shell < insert_default_records.py
    - 6. python3 manage.py runserver [ip]:[port]
    - 7. Connect to [ip]:[port] to see the page.

- Testing steps:
    - python3 manage.py test

