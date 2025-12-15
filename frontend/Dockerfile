# syntax=docker/dockerfile:1
FROM nginx:1.27-alpine

# Copy Nginx config and static assets
COPY frontend/nginx.conf /etc/nginx/nginx.conf
COPY frontend/index.html /usr/share/nginx/html/index.html
COPY frontend/diary.html /usr/share/nginx/html/diary.html
COPY frontend/view-diary.html /usr/share/nginx/html/view-diary.html

EXPOSE 80
