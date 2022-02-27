FROM nginx:alpine 

RUN sed -i -e '/location.*\/.*{/a autoindex on\;' /etc/nginx/conf.d/default.conf

COPY . /usr/share/nginx/html