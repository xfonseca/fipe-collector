FROM python:3.6

ADD . /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

CMD python app/app.py