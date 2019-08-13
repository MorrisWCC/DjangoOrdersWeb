FROM python:3
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /code/

CMD ["python3", "manage.py", "collectstatic"]
CMD ["python3", "manage.py", "migrate"]
CMD ["python3", "manage.py", "makemigrations"]
CMD ["python3", "manage.py", "<", "insert_default_records.py"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

