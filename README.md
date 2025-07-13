### Database Setup

Install postgresql via conda
```sh
conda Install postgresql==12.2
```

Create db
```sh
initdb -D "C:\Local\Path\EmptyFolder"
```

Update datetime format configuration
```sh
C:\Local\Path\EmptyFolder\postgresql.conf:
SET datestyle = 'iso, mdy'
```

Start DB
```sh
pg_ctl.exe start -D "C:\Local\Path\EmptyFolder"
or
pg_ctl.exe restart -D "C:\Local\Path\EmptyFolder"
```

Create User
```sh
createuser.exe -W docker
```

Create databases
```sh
createdb -O docker dhs
```

Create schema
```sh
psql -d dhs -c "CREATE SCHEMA IF NOT EXISTS \"FININC_OWNER\"; GRANT ALL PRIVILEGES ON SCHEMA \"FININC_OWNER\" to docker;"
psql -d dhs "CREATE ROLE \"FININC_USER\";"
```

Drop schema
```sh
psql -d dhs -c "DROP SCHEMA \"FININC_OWNER\" CASCADE;"
```

Drop Role
```sh
psql -d dhs -c "DROP ROLE IF EXISTS \"FININC_USER\";"
```

### Code check

Before pushing your changes to the repository please run a linter and code formatting
```sh
isort hack_rest --profile=black && python -m black -t py39 hack_rest && python -m pylint -j 1 hack_rest
```

### Windows config

A few environment variables have to be setup to make flask work locally. These are automatically read from the `.flaskenv` file by the `python-dotenv` library.
However, they can be overrideen if needed as below:

```sh
SET FLASK_APP=hack_rest\app.py
SET FLASK_ENV=development
SET FLASK_HOST=0.0.0.0
set FLASK_DEBUG=1
```