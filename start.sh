#!/bin/bash

python -m spacy download en_core_web_sm
python -m spacy download en_core_web_trf
gunicorn --worker-class eventlet -w 1 app:app
