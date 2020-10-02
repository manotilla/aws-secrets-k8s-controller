FROM python:alpine
RUN apk update && apk add busybox-extras build-base
COPY requirements.txt .
COPY cmd /controller/
RUN pip3 install -r requirements.txt
WORKDIR /controller/
ENTRYPOINT python3 main.py