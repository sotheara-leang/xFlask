#!/usr/bin/env bash

CONF_FILE=$1

PORT=`cat $CONF_FILE | shyaml get-value PORT`

lsof -n -i4TCP:$PORT | grep LISTEN | awk '{ print $2 }' | xargs kill
