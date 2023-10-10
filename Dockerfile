FROM python:latest
ADD DespKafka /app/DespKafka
ADD etc /app/etc
ADD requirements-docker.txt /app/requirements.txt
RUN cd /app && pip install -r requirements.txt
WORKDIR /app
ENTRYPOINT [ "python" ]