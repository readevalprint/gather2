FROM ubuntu:14.04

ENV TERM screen-256color

RUN locale-gen --no-purge en_US.UTF-8
ENV LC_ALL en_US.UTF-8
RUN update-locale LANG=en_US.UTF-8

RUN apt-get update -qq && apt-get install -y wget
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main 9.4" > /etc/apt/sources.list.d/pgdg.list

ADD conf/apt-packages.txt /tmp/apt-packages.txt
RUN apt-get update -qq && cat /tmp/apt-packages.txt | xargs apt-get --yes --force-yes install

ADD requirements.txt /tmp/requirements.txt
RUN pip3 install virtualenv

RUN virtualenv -p python3 /var/env/
RUN /var/env/bin/pip install -r /tmp/requirements.txt

WORKDIR /code/

COPY ./ /code

ENTRYPOINT ["bash", "/code/entrypoint.sh"]
