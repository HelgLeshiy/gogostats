FROM python:3.10-slim

ADD ./requirements.txt /opt/gogoclient/requirements.txt

WORKDIR /opt/gogoclient
RUN pip install -r requirements.txt

ADD . /opt/gogoclient

CMD ["python", "main.py"]