FROM --platform=$BUILDPLATFORM node:22-bookworm-slim AS builder

ARG UI_VERSION=2.6.0

RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates python3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src
RUN git clone --depth 1 --branch "${UI_VERSION}" https://github.com/Joxit/docker-registry-ui.git .

COPY apply-branding.py /tmp/apply-branding.py
COPY oscriscloud-registry-logo.svg /src/src/oscriscloud-registry-logo.svg
COPY oscriscloud-registry-favicon.svg /src/src/oscriscloud-registry-favicon.svg

RUN python3 /tmp/apply-branding.py
RUN npm install
RUN npm run build

RUN cp /src/src/oscriscloud-registry-logo.svg /src/dist/ \
    && cp /src/src/oscriscloud-registry-favicon.svg /src/dist/

FROM debian:bullseye-slim

RUN set -eux; \
    printf '%s\n' \
      'deb http://archive.debian.org/debian bullseye main' \
      'deb http://archive.debian.org/debian bullseye-updates main' \
      'deb http://archive.debian.org/debian-security bullseye-security main' \
      > /etc/apt/sources.list; \
    printf '%s\n' 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99archive; \
    apt-get update; \
    apt-get install -y --no-install-recommends nginx ca-certificates; \
    rm -rf /var/lib/apt/lists/*; \
    rm -f /etc/nginx/sites-enabled/default; \
    rm -rf /usr/share/nginx/html/*

WORKDIR /usr/share/nginx/html

COPY --from=builder /src/dist/ /usr/share/nginx/html/
COPY --from=builder /src/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /src/bin/90-docker-registry-ui.sh /docker-entrypoint.d/90-docker-registry-ui.sh
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh /docker-entrypoint.d/90-docker-registry-ui.sh \
    && sed -i 's/\r$//' /entrypoint.sh /docker-entrypoint.d/90-docker-registry-ui.sh

ENV NGINX_PROXY_HEADER_Host='$http_host' \
    NGINX_LISTEN_PORT='80' \
    NGINX_PROXY_PASS_URL='http://registry:5000' \
    NGINX_RESOLVER='127.0.0.11' \
    SINGLE_REGISTRY='true' \
    REGISTRY_TITLE='OsCrisCloud Docker Registry' \
    DOCKER_REGISTRY_UI_TITLE='OsCrisCloud Docker Registry' \
    REGISTRY_URL='' \
    PULL_URL='192.168.178.130:5000' \
    DELETE_IMAGES='true' \
    SHOW_CONTENT_DIGEST='true' \
    SHOW_CATALOG_NB_TAGS='true' \
    SHOW_TAG_HISTORY='true' \
    CATALOG_ELEMENTS_LIMIT='1000' \
    CATALOG_DEFAULT_EXPANDED='false' \
    CATALOG_MIN_BRANCHES='1' \
    CATALOG_MAX_BRANCHES='1' \
    TAGLIST_PAGE_SIZE='100' \
    TAGLIST_ORDER='alpha-asc;num-desc' \
    REGISTRY_SECURED='false' \
    USE_CONTROL_CACHE_HEADER='false' \
    DEFAULT_REGISTRIES='' \
    READ_ONLY_REGISTRIES='false' \
    HISTORY_CUSTOM_LABELS='' \
    ENABLE_VERSION_NOTIFICATION='false' \
    THEME='auto'

EXPOSE 80
ENTRYPOINT ["/entrypoint.sh"]
