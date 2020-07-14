FROM mariadb:latest as builder

RUN ["sed", "-i", "s/exec \"$@\"/echo \"not running $@\"/", "/usr/local/bin/docker-entrypoint.sh"]

ENV MYSQL_ROOT_PASSWORD=root
RUN python3 main.py &&
    apt install sqlite3 &&
    sqlite3 anime.db .dump >> anime.sql

COPY anime.sql /docker-entrypoint-initdb.d/

RUN ["/usr/local/bin/docker-entrypoint.sh", "mysqld", "--datadir", "/initialized-db", "--aria-log-dir-path", "/initialized-db"]

FROM mariadb:latest

COPY --from=builder /initialized-db /var/lib/mysql