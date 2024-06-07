FROM python:3.12

RUN apt-get update && apt-get install

RUN mkdir /app

WORKDIR /app

COPY docker/requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

