#!/usr/bin/env bash
gen_fingerprint () {
    for file in $(ls $1/*.pub)
    do
        ssh-keygen -lf $file
    done
}

gen_fingerprint /etc/ssh
gen_fingerprint /home/sam/.ssh
