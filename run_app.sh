#!/bin/bash

cd src

python app.py 0 0.5

python app.py 00 0.7
python app.py 01 0.6
python app.py 02 0.5
python app.py 03 0.4
python app.py 04 0.3
python app.py 05 0.2
python app.py 06 0.1
python app.py 07 0.0

python app.py 000 0.7
python app.py 001 0.6
python app.py 002 0.5
python app.py 003 0.4
python app.py 004 0.3
python app.py 005 0.2
python app.py 006 0.1
python app.py 007 0.0

python app.py 0000 0.7
python app.py 0001 0.6
python app.py 0002 0.5
python app.py 0003 0.4
python app.py 0004 0.3
python app.py 0005 0.2
python app.py 0006 0.1
python app.py 0007 0.0

mv ../output/*.b3dm ../../threejs-vite-starter/static

# pip freeze > requirements.txt