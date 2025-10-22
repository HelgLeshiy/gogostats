FROM python:3.10-slim

ADD ./requirements.txt /opt/gogoproxy/requirements.txt

WORKDIR /opt/gogoproxy
RUN pip install -r requirements.txt

ADD . /opt/gogoproxy

EXPOSE 5800

CMD ["mitmdump", "-s", "tcpaddon.py", "--mode", "socks5@5800", "--set", "block_global=false", "--set", "connection_strategy=lazy"]