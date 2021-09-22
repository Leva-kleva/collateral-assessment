FROM nginx:latest

COPY ./nginx.conf /etc/nginx/nginx.conf

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
