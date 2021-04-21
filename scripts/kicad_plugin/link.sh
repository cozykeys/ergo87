#!/usr/bin/env bash

function link_simple() {
    script_dir="$( dirname "$(realpath $0)" )"

    plugins_dir="$HOME/.kicad_plugins"
    mkdir -p "$plugins_dir"

    src="$script_dir/bloomer_kicad_plugin_action.py"
    dst="$plugins_dir/bloomer_kicad_plugin_action.py"

    if [ -e "$dst" ]; then
        1>&2 echo "Destination \"$dst\" already exists!"
        exit 1
    fi

    echo "Creating symlink from $dst to $src" 
    ln -s "$src" "$dst"
}

link_simple

