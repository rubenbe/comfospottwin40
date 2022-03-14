FROM alpine:3.15
RUN apk add python3 py3-pip
ADD . /comfospot
RUN pip install -r /comfospot/requirements.txt
CMD python3 /comfospot/server.py
