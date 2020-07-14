FROM postgres
ENV POSTGRES_DB my_database

COPY anime-offline-database.json ./
RUN python3 main.py &&
    apt install sqlite3 &&
    sqlite3 anime.db .dump >> anime.sql
COPY psql_dump.sql /docker-entrypoint-initdb.d/
RUN rm anime-* anime*



