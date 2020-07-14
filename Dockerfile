FROM postgres:12.3-alpine
ENV POSTGRES_DB hanako
COPY anime.sql /docker-entrypoint-initdb.d/