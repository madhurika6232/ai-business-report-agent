#!/bin/sh
set -eu

if [ -z "${RETAILOPS_API_KEY:-}" ]; then
    echo "ERROR: RETAILOPS_API_KEY is required."
    exit 1
fi

escaped_key="$(printf '%s' "$RETAILOPS_API_KEY" | sed 's/[\/&]/\\&/g')"

sed \
    "s/__RETAILOPS_API_KEY__/${escaped_key}/g" \
    /etc/nginx/templates/retailops.conf.template \
    > /etc/nginx/conf.d/default.conf

exec nginx -g "daemon off;"