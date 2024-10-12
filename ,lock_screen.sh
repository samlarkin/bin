#!/usr/bin/env bash
tmpbg="/tmp/screen.png"
scrot -F "$tmpbg"
convert "$tmpbg" -scale 10% -scale 1000% "$tmpbg"
i3lock -u -i "$tmpbg"
