FROM python:3.7.9

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt-get update -y

RUN apt-get install -y    libssl-dev

RUN apt-get update && apt-get install -y \
        libsasl2-dev\
        python-dev \
        libldap2-dev \
        libssl-dev \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./pip.conf /etc/pip.conf

ENV TZ=Asia/Shanghai \
    FLASK_CONFIG=default

RUN pip install --no-cache-dir --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt