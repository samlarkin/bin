#!/bin/sh
weather=$(curl -s 'wttr.in/?format=3')
echo $weather

