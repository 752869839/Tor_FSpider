FROM ubuntu:18.04
RUN sed -i -e 's/archive\.ubuntu\.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list
RUN sed -i -e 's/security\.ubuntu\.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list
ADD . /code
WORKDIR /code
RUN  mkdir -p /code/login/img

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y vim unzip

ENV TZ 'Asia/Shanghai'
RUN echo $TZ > /etc/timezone
RUN apt-get install tzdata
RUN rm -f /etc/localtime && ln -sf /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata
RUN apt-get install locales
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen

RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip

COPY ./scrapyd.conf /etc/scrapyd/
COPY ./clean.sh /code/
COPY ./scrapyd_monitor.sh /code/
COPY ./requirements.txt /code/

RUN apt-get install -y libcairo2-dev
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


EXPOSE 5000
EXPOSE 6800
EXPOSE 6801

CMD /bin/bash

