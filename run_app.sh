#!/bin/bash

cd src

python app.py

mv ../output/* ../../threejs-vite-starter/static

# pip freeze > requirements.txt