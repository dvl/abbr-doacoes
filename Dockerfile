FROM python:3.5

RUN mkdir -p /usr/src/app

ENV PATH /usr/src/env/bin:$PATH

WORKDIR /usr/src/app

RUN pip install -U pip
RUN pip install virtualenv

RUN virtualenv /usr/src/env

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
