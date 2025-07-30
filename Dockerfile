FROM debian:bullseye-slim

RUN apt update && apt install -y python3 python3-pip curl bash

COPY mtproxy_plus.py /opt/mtproxy_plus.py
COPY bin/mtg /usr/local/bin/mtg

WORKDIR /opt

ENV PROXY_SECRET=abcdef0123456789abcdef0123456789
ENV PORT_START=30000
ENV PORT_END=30010
ENV TLS_DOMAIN=www.cloudflare.com

CMD ["python3", "/opt/mtproxy_plus.py"]
