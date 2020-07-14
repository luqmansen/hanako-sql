import json
import os
import sqlite3
from datetime import datetime
from sqlite3 import IntegrityError


def quotify(s):
    return '"' + s.strip().replace('"', '""') + '"'


def init_schema(con):
    tables = ["anime", "sources", "synonyms", "relations"]
    for i in tables:
        con.execute("drop table if exists {};".format(quotify(i)))

    con.execute("drop table if exists animes;")
    con.execute("create table animes (id int primary key,title varchar(255),type varchar(255),episodes int,"
                "status varchar(255), picture varchar(255),thumbnail varchar(255));")
    con.execute(
        "create table sources (id integer primary key AUTOINCREMENT,url varchar(255),anime_id int, foreign key ( "
        "anime_id) references animes(id));")
    con.execute(
        "create table synonyms (id integer primary key AUTOINCREMENT,name varchar(255),anime_id int, foreign key ("
        "anime_id) references animes(id));")
    con.execute(
        "create table relations (id integer primary key AUTOINCREMENT,url varchar(255),anime_id int, foreign key ("
        "anime_id) references animes(id));")


def process_row(row_id, con):
    try:
        row = data[row_id]
        if row_id % 1000 == 0:
            print("Processing row id {}".format(row_id))

        con.execute("insert into animes (id, title, type, episodes, status, picture, thumbnail) values({},{},{},{},"
                    "{},{},{})".format(row_id, quotify(row['title']), quotify(row['type']), row['episodes'],
                                       quotify(row['status']), quotify(row['picture']), quotify(row['thumbnail'])))
        for url in row["sources"]:
            con.execute("insert into sources (url, anime_id) values({},{})".format(quotify(url), row_id))
        for url in row["relations"]:
            con.execute("insert into relations (url, anime_id) values({},{})".format(quotify(url), row_id))
        for name in row["synonyms"]:
            con.execute("insert into synonyms (name, anime_id) values({},{})".format(quotify(name), row_id))
        con.commit()
        return
    except IndexError or IntegrityError:
        return
    except sqlite3.OperationalError or sqlite3.ProgrammingError:  # sometimes there is a database lock
        process_row(row_id, con)
    except Exception as e:
        print("Error in processing row {} with error {}".format(row_id, str(e)))
        return


def main():
    start = datetime.now()
    global data
    with open('anime-offline-database.json') as file:
        data = json.load(file).get("data")
    # here is super fast in memory db, no need multi processing /
    # threading since can't share same conn for in memory db
    conn = sqlite3.connect("file::memory:?cache=shared")

    init_schema(conn)
    for i in range(len(data)):
        process_row(i, conn)
    print("Processing done, writing to file...")
    c2 = sqlite3.connect('anime.db')
    with c2:
        for line in conn.iterdump():
            if line not in ('BEGIN;', 'COMMIT;'):
                c2.execute(line)
    c2.commit()
    print("Inserted {} with elapsed time {} ".format(len(data), datetime.now() - start))


if __name__ == '__main__':
    main()
    os.system("sqlite3 anime.db .dump >> anime.sql")
