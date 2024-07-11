FROM python:3.12.3

WORKDIR /cv-indexing

COPY . .

RUN pip install -r ./configure/requirements.txt