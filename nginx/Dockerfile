FROM nginx:1.21-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY uwsgi_params /etc/nginx/uwsgi_params
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
