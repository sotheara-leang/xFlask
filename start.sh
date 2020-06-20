#!/usr/bin/env bash

CONF_FILE=$1

HOST=`cat $CONF_FILE | shyaml get-value HOST`
PORT=`cat $CONF_FILE | shyaml get-value PORT`

gunicorn --bind $HOST:$PORT main.server:app
# python -m main.server
