# hanako-sql

[![Update Automation](https://github.com/luqmansen/hanako-mongodb/workflows/Update%20Automation/badge.svg)](https://github.com/luqmansen/hanako-postgresql/actions)
[![Docker Pulls](https://img.shields.io/docker/pulls/luqmansen/hanako-postgresql)](https://hub.docker.com/r/luqmansen/hanako-postgresql)
[![Size](https://img.shields.io/docker/image-size/luqmansen/hanako-postgresql)](https://hub.docker.com/r/luqmansen/hanako-postgresql)

Docker image version of  [manami-project/anime-offline-database](https://github.com/manami-project/anime-offline-database). Pre-seeded inside postgresql image, ready to use.


CI Scheduled to update everyday  even though the upstream updated  every week.

## Run 
```
 docker run \
    --name hanako \ 
    -e POSTGRES_PASSWORD=mysecretpassword \ 
    luqmansen/hanako-postgresql
```