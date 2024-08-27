FROM python:3.10-slim-bullseye

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN apt-get -y update

COPY requirements.txt .
RUN python -m pip install --disable-pip-version-check --no-cache-dir -r requirements.txt

COPY . tests/functional

ENV PYTHONPATH=/opt/app

CMD ["sh", "-c", "python3 tests/functional/utils/wait_for_es.py && python3 tests/functional/utils/wait_for_redis.py && pytest tests/functional/src"]
