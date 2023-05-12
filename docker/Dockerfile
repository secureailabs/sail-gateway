FROM ubuntu:20.04

ENV TZ=America/Toronto
LABEL authors="prawal@secureailabs.com"
USER root

# Set time zone data
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install nginx and python
RUN apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y \
  curl \
  nginx \
  lsb-release \
  python3 \
  python3-pip

# Install redis
RUN curl -fsSL https://packages.redis.io/gpg | gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/redis.list
RUN apt-get update
RUN apt-get install -y redis

# Install poetry
RUN pip3 install poetry

# Install dependencies
COPY poetry.lock pyproject.toml /
RUN poetry config virtualenvs.create false && poetry install

RUN apt-get install dnsutils -y

# Copy the application
COPY dns-server /app

# Copy the nginx configuration
COPY nginx/nginx.conf /etc/nginx/nginx.conf

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


ENTRYPOINT [ "/entrypoint.sh" ]
