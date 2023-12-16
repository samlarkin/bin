#!/usr/bin/env bash
let loop=0
while true; do
    if [[ $loop%300 -eq 0 ]]; then
        myip=$(/home/sam/bin/,myip.sh)
        weather=$(/home/sam/bin/,weather.sh)
        let loop=0
    fi
    xsetroot -name " $weather | $myip | $(date '+%Y-%m-%d') | $(date '+%H:%M') "
    sleep 1
done
