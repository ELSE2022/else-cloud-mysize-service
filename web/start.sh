#!/usr/bin/env bash

sleep 10

if [ $DEBUG = "true" ]; then
    echo "[START] launch app in debug mode"
    python start.py
else
    echo "[START] collect static resources"
    gunicorn -w 20 -t 120 -b 0.0.0.0:5000 wsgi
fi


