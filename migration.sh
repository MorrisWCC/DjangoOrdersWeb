#!/bin/bash
python3 manage.py migrate
python3 manage.py shell < insert_default_records.py
python3 manage.py runserver 0.0.0.0:8000
