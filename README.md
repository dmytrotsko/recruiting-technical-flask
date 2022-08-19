# Delphi Flask API Take-home

## Start the Database Container

Start the database with the following command:

    docker run --rm -p 3306:3306 -e MYSQL_ROOT_PASSWORD=strong_password -e MYSQL_DATABASE=delphi -e MYSQL_USER=foo -e MYSQL_PASSWORD=bar -v $(pwd)/database/init/:/run/init -v $(pwd)/database/my.cnf:/etc/mysql/my.cnf --name cheese_database mysql:latest

In a separate terminal, run the following command to populate the database.

    docker exec cheese_database /bin/sh -c 'chmod +x /run/init/initialize_database.sh && ./run/init/initialize_database.sh'