FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    python3 \
    python3-pip \
    python3-venv \
    redis-server \
    && rm -rf /var/lib/apt/lists/*

RUN rm /var/www/html/* 
RUN pip3 install --no-cache-dir gunicorn flask redis requests

WORKDIR /app

COPY app ./
COPY start.sh /root/start.sh

RUN chmod a+x /root/start.sh

COPY flask_app.conf /etc/nginx/sites-available/flask_app
RUN rm /etc/nginx/sites-enabled/default && \
    ln -s /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled/

CMD [ "/root/start.sh" ]
