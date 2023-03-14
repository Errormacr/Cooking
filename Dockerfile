FROM python:3.8
RUN mkdir /cook_app

WORKDIR /cook_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
RUN chmod a+x docker/*.sh
#WORKDIR server
#
#CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000