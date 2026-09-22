# ============================================================
# Build stage
# ============================================================

FROM node:24-alpine AS build

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

ARG VITE_API_BASE_URL=""

ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build


# ============================================================
# Runtime stage
# ============================================================

FROM nginx:1.29-alpine

COPY --from=build /app/dist /usr/share/nginx/html

COPY nginx.conf.template \
    /etc/nginx/templates/retailops.conf.template

COPY docker-entrypoint.sh \
    /usr/local/bin/retailops-entrypoint.sh

RUN chmod +x \
    /usr/local/bin/retailops-entrypoint.sh

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q -O /dev/null http://127.0.0.1/health || exit 1

ENTRYPOINT ["/usr/local/bin/retailops-entrypoint.sh"]