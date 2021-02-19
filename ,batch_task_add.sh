#!/bin/sh

project="$1"
descriptions_file="$2"


function add_task() {
    # Add a task to taskwarrior database, using the task add command.

    local description="$1"
    task project:"$project" "$description"
}


function main() {
    # Read list of task descriptions from a file and add each one.

    for line in $(< "$descriptions_file")
    do
        add_task "$line"
    done
}


main
