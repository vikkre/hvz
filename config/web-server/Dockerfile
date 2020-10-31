FROM node:12

WORKDIR /app

COPY ./frontend/web/ /app/web
COPY ./frontend/package*.json /app/

RUN npm install
RUN npm run build


FROM nginx:latest

COPY --from=0 /app/dist /www
COPY ./config/web-server/production-nginx.conf /etc/nginx/nginx.conf
