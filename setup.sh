#!/bin/sh
virtualenv . --no-site-packages && source Scripts/activate && pip install -r requirements.txt
