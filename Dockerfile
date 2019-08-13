FROM python:3
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
COPY migration.sh /code/
RUN pip3 install -r requirements.txt
RUN chmod +x /code/migration.sh
COPY . /code/

