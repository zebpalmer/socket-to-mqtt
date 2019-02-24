# Base Image
FROM python:3.7-slim-stretch as base

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

# STAGE: final
FROM base as final


COPY /scripts/socket-consumer.py /socket-consumer.py



CMD ["python3", "socket-consumer.py"]