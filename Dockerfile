FROM python:3.6-slim

ENV INSTALL_PATH /app
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

ENV DOCKER_HOST=127.0.0.1:8000
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "run:app"
