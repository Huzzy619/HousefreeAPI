#!/bin/sh

echo Collecting Staticfiles

python3  manage.py collectstatic --no-input

python3 manage.py super

