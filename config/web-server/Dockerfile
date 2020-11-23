FROM node:12

WORKDIR /app

# First do the steps that might be the same in most builds, so we can profit from caching as much as possible
COPY ./frontend/package*.json /app/
RUN npm install

COPY ./frontend/web/ /app/web
RUN npm run build

FROM nginx:latest

COPY --from=0 /app/dist /www
COPY ./config/web-server/production-nginx.conf /etc/nginx/nginx.conf
