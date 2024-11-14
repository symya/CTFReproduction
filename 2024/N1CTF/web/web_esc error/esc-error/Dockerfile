FROM python:3.10-slim

RUN echo 'deb https://mirrors.aliyun.com/debian/ bookworm main non-free non-free-firmware contrib' >> /etc/apt/sources.list && \
    echo 'deb https://mirrors.aliyun.com/debian-security/ bookworm-security main' >> /etc/apt/sources.list && \
    rm -rf /etc/apt/sources.list.d

RUN apt-get update && apt-get install -y \
    mariadb-server \
    pkg-config \
    libmariadb-dev \
    libssl-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY files/requirements.txt /

RUN pip install -r /requirements.txt

COPY src /var/ 
COPY files/run.sh files/readflag.c /
COPY files/supervisord.conf /etc/supervisor/

RUN useradd -m -d /home/ctf ctf && \
    chmod 444 /home/ctf/.bashrc && chmod 444 /home/ctf/.profile && chmod 444 /home/ctf/.bash_logout && \
    chown -R ctf:ctf /var/lib/mysql && \
    mkdir -p /run/mysqld && \ 
    chown -R ctf:ctf /run/mysqld && \
    rm /etc/mysql/mariadb.conf.d/provider_* && \
    echo 'plugin_dir=/home/ctf/lib/plugins' >> /etc/mysql/mariadb.conf.d/50-server.cnf

WORKDIR /var/www/app/

# Set test_mod `on` to disable the hash check
# ENV test_mod=on

CMD ["bash", "/run.sh"]