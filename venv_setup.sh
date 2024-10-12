#!/usr/bin/bash
# Takes one argument - venv name
python3 -m venv ~/env/$1
source ~/env/$1/bin/activate
~/env/$1/bin/pip3 install ipykernel jupyterlab
~/env/$1/bin/python3 -m ipykernel install --name $1 --user
