FROM ubuntu:22.04 as base

RUN apt-get -yqq update
RUN apt-get -yqq install software-properties-common
RUN apt-get -yqq update
RUN apt-get -yqq install python3.10
RUN apt-get -yqq install python3-pip
RUN apt-get -yqq install python-is-python3

RUN pip install --upgrade pip
ADD ./requirements.txt /opt/gogo-backend/requirements.txt

WORKDIR /opt/gogo-backend
RUN pip install -r requirements.txt

ADD . /opt/gogo-backend

EXPOSE 5997

CMD ["flask", "--app", "main", "run", "--port=5997", "--host=0.0.0.0"]