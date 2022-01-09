FROM python:3
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/ 

RUN adduser --disabled-password --no-create-home django-user

USER django-user