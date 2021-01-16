#!/bin/sh
let loop=0
while true; do
    if [[ $loop%300 -eq 0 ]]; then
        myip=$(curl http://ipecho.net/plain; echo)
        let loop=0
    fi
    xsetroot -name " $myip | $(date '+%Y-%m-%d') | $(date '+%H:%M') "
    sleep 1
done
