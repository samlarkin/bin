#!/bin/sh

# Compiling script for generating html copies of all of the markdown
# files in my notes directory.
#
# Relies on pandoc for conversion from markdown to html.
#
# Author: Sam Larkin
# Date: 2021-02-11



function list_files() {
    # List the files in the directory at $path, which have the
    # extension $ext. Store the resulting list in an array $files.

    local ext=$1

    files=($(ls $path | grep $ext))
}


function make_index_entry() {
    # Make a link in markdown format by extracting the title from a
    # .md file and renaming it to *.html. Append the index entry to
    # index.md.
    
    local file=$1

    local title=$(grep "title: " $path/$file | cut -d: -f2 | sed s/.//)
    local html_file=$(echo "$file" | sed s/.md/.html/)

    echo "* [$title]($html_file)" >> $index
}


function generate_html() {
    # Call pandoc to convert markdown file to both a plain html file
    # and a standalone html file, styled using the $css style sheet.

    local file=$1

    local input=$path/$file
    local html_file=$(echo "$file" | sed s/.md/.html/)
    local plain=$path/compiled/plain/$html_file
    local css=$path/compiler/style.css
    local standalone=$path/compiled/standalone/$html_file

    pandoc -o $plain $input &
    pandoc -s -c $css -o $standalone $input &
}


function main() {
    # Overwrite the index file, then list the markdown files in the
    # notes directory. Loop over the list and append an entry for each
    # file to the index. Finally, compile html files from the md file.

    local path="$HOME/notes"
    local index=$path/index.md
    local template=$path/compiler/index_template

    cat $template > $index
    list_files '.md'

    for file in ${files[@]}
    do
        echo "Making index entry for ... $file"
        make_index_entry $file
        echo "Compiling ... $file"
        generate_html $file
    done
}


main
exit 0
