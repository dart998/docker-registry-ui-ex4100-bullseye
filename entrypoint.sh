#!/bin/sh
set -e

cd /usr/share/nginx/html
/docker-entrypoint.d/90-docker-registry-ui.sh

exec nginx -g 'daemon off;'
