#!/bin/bash
set -e

# Copy the root domain from the the initialization vector json file
ROOT_DOMAIN=$(cat /InitializationVector.json | jq -r '.root_domain')
sed -i "s/\${ROOT_DOMAIN}/$ROOT_DOMAIN/g" /etc/nginx/nginx.conf

# Start the nginx server
nginx -g 'daemon off;' 2>&1 | tee /app/nginx.log &

# Start the redis server
redis-server --daemonize yes

# Start the Public API Server
uvicorn app.dns_crud:app --host 0.0.0.0 --port 8000 &

# Start the DNS resolver
python3 app/dns_resolution.py &

# To keep the container running
tail -f /dev/null
