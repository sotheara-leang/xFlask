Notes:
    1. Every command is run from the root directory


------------------------------------------------------------------

1. Environment

python3 -m venv /path/to/new/virtual/environment

pip install -r requirement.txt

pip install --upgrade xFlask

2. Configuration

There are two configuration files located in main/conf
    - server.yml:   server configuration file
    - logging.yml:  logging configuration file

3. Migration

python -m main.migrate db init

python -m main.migrate db migrate

python -m main.migrate db upgrade

Notes:
    1. The customized enum must be included in maing/migration_types.py
    2. In case you use customized enum, you need to modify the generated script before running db upgrade

4. Server

python -m main.server

FLASK_APP=main.server:app python -m flask run -p 8000

gunicorn main.server:app