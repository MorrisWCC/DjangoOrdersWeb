FROM python:3
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
COPY migration.sh /code/
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["migration.sh"]
COPY . /code/


