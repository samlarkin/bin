#!/usr/bin/env bash
weather=$(curl -s "wttr.in/?format=%l:+%C+%t")
echo $weather
