#!/bin/bash
set -e
apt update && apt install -y docker.io
systemctl enable docker && systemctl start docker
docker build -t mtproxy-tls .
docker run -d \
  --name mtproxy-tls \
  -e PROXY_SECRET=abcdef0123456789abcdef0123456789 \
  -e PORT_START=30000 \
  -e PORT_END=30010 \
  -e TLS_DOMAIN=www.cloudflare.com \
  -p 30000-30010:30000-30010 \
  mtproxy-tls
