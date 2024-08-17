#The base image for the container 
FROM python:3.12-slim-bullseye

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE=1 

ENV PYTHONUNBUFFERED=1 

RUN apt-get -y update

COPY requirements.txt . 
RUN python -m pip install -r requirements.txt 

COPY ./src .

RUN chmod +x ./main.py

RUN groupadd -r app_group \
    && useradd -d /opt/app -r -g app_group app \
    && chown app:app_group -R /opt/app/ \
    && chown app:app_group -R /var/log/ 

USER app

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000","-k","uvicorn.workers.UvicornWorker", "main:app"]