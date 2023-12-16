#!/bin/sh

# Author: Sam Larkin
# Date: 2021-02-11

# on-launch.backup.sh
# This hook script for taskwarrior runs on launch and backs up data
# from taskwarrior and timewarrior before any modifications are made.

function backup_dir() {
    # Backup data from src directory to dst directory and echo
    # msg to STDERR.
    src=$1
    dst=$2

    msg="backing up ... $src ... to ... $dst"
    1>&2 echo $msg
    cp -r $src $dst
}


function main() {
    # Backup data for taskwarrior and timewarrior.
    backup_dir $HOME/.task $HOME/bak/task
    backup_dir $HOME/.timewarrior $HOME/bak/timewarrior
}


main
exit 0
