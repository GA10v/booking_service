#!/bin/sh
gunicorn --bind 0.0.0.0:8084 -w 4 -k uvicorn.workers.UvicornH11Worker main:app