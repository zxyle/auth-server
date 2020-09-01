FROM python:3.7.9

WORKDIR /usr/src/app

RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list && \
    sed -i s@/security.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
        libsasl2-dev\
        libldap2-dev \
        libssl-dev \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./pip.conf /etc/pip.conf

ENV TZ=Asia/Shanghai \
    FLASK_CONFIG=default

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt