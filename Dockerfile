FROM alpine:3.18
RUN apk add python3 py3-pip
ADD . /comfospot
RUN pip install -r /comfospot/requirements.txt
ENTRYPOINT ["/comfospot/server.py"]
