# Nginx Proxy

## Build the service
```
docker build -t nginx-proxy -f docker/Dockerfile .
```

# Run the built service
```
docker run -it -v $(pwd)/certs:/etc/nginx/certs -p 8000:8001 -p 80:80 -p 443:443 nginx-proxy
```
