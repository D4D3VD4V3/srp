FROM python:3.6-alpine3.6

ENV INSTALL_PATH /app
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

#pip install --upgrade setuptools
#easy_install --upgrade requests
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "run:app"
