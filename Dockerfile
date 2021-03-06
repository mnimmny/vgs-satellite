FROM node:14.15.1-alpine3.12

RUN apk update && apk add --no-cache \
    musl-dev \
    build-base \
    libxslt-dev \
    libffi-dev \
    openssl-dev \
    git \
    python3-dev \
    py3-pip

WORKDIR /satellite

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN npm ci --unsafe-perm

EXPOSE 8089 9098 9099 1234

VOLUME /data

ENV SATELLITE_DIR=/data
ENV SATELLITE_WEB_PORT=1234
ENV SATELLITE_API_PORT=8089
ENV SATELLITE_REVERSE_PROXY_PORT=9098
ENV SATELLITE_FORWARD_PROXY_PORT=9099

ENTRYPOINT ["npm", "run", "start:docker"]
