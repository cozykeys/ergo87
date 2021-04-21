#!/usr/bin/env bash

action="$1"

bloomer_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# TODO: Is there a better way? Submodule perhaps?
kbutil_dir="$( dirname "$bloomer_dir" )/kbutil"

kbutil_dll="$kbutil_dir/build/KbUtil.Console/bin/Release/kbutil.dll"
kbmath_dll="$kbutil_dir/build/KbMath.Console/bin/Release/KbMath.Console.dll"

svg_opener="inkscape"

function error() {
    local msg="$1"

    local COLOR_NONE='\033[0m'
    local COLOR_ERROR='\033[0;31m'

	>&2 echo -e "${COLOR_ERROR}ERROR: $msg${COLOR_NONE}"
    exit 1
}

function generate_render() {
    input="$bloomer_dir/bloomer.xml"
    output="$bloomer_dir/case"


    options="--visual-switch-cutouts --keycap-overlays --keycap-legends --squash"

    dotnet "$kbutil_dll" gen-svg $options "$input" "$output"
    dotnet "$kbutil_dll" gen-key-bearings "$input" "./temp/keys.json" --debug-svg="./temp/bearings.svg"

    "$svg_opener" "$output/bloomer.svg"
}

function generate_case() {
    input="$bloomer_dir/bloomer.xml"
    output="$bloomer_dir/case"


    options="--visual-switch-cutouts --keycap-overlays --keycap-legends"

    dotnet "$kbutil_dll" gen-svg $options "$input" "$output"
    dotnet "$kbutil_dll" gen-key-bearings "$input" "./temp/keys.json" --debug-svg="./temp/bearings.svg"

    "$svg_opener" "$output/bloomer_switch.svg"
}

function generate_ponoko() {
    input="$bloomer_dir/bloomer.xml"
    output="$bloomer_dir/case/ponoko"

    dotnet "$kbutil_dll" gen-svg $options "$input" "$output"

    "$svg_opener" "$output/bloomer_Switch.svg" 
}

function generate_perimeters() {
    local vertices_file="pcb_edge_vertices.json"
    [ ! -f "$vertices_file" ] && \
        1>&2 echo "Vertices file $vertices_file does not exist" && \
        exit 1

    mkdir -p "temp"

    # Generate the inner perimeter
    dotnet "$kbmath_dll" expand-vertices \
        --debug-svg="temp/inner_perimeter.svg" \
        "$vertices_file" \
        "temp/inner_perimeter.json" \
        1.5

    # Generate the outer perimeter
    dotnet "$kbmath_dll" expand-vertices \
        --debug-svg="temp/outer_perimeter.svg" \
        "$vertices_file" \
        "temp/outer_perimeter.json" \
        11.5

    # Generate the outer perimeter curves
    dotnet "$kbmath_dll" generate-curves \
        --output-xml="temp/outer_perimeter_curves.xml" \
        --debug-svg="temp/outer_perimeter_curves.svg" \
        "temp/outer_perimeter.json" \
        "temp/outer_perimeter_curves.json" \
        3

    "$svg_opener" \
        "temp/inner_perimeter.svg" \
        "temp/outer_perimeter.svg" \
        "temp/outer_perimeter_curves.svg"
}

function generate_pcb() {
    pcb_dir="$bloomer_dir/pcb"

    input="$bloomer_dir/switches.json"
    output="$pcb_dir/bloomer.kicad_pcb"

    (
        cd "$kbutil_dir"
        make
    )

    mkdir -p "$pcb_dir"
    dotnet "$kbutil_dll" gen-pcb "bloomer" "$input" "$output"
}

function generate_traces() {
    error "Not yet implemented"
}

function print_usage() {
    echo "USAGE: ./bloomer.sh <action> [OPTIONS]"
    echo ""
    echo "Actions:"
    echo "    generate-render       : Generate an svg render of the keyboard"
    echo "    generate-case         : Generate svg renders of the keyboard case layers"
    echo "    generate-ponoko       : Generate an svg styled to be cut by Ponoko"
    echo "    generate-perimeters   : Calculate case perimeters based on PCB edge cuts"
    echo "    generate-pcb          : Generate a kicad_pcb file from kbutil templates"
    echo "    generate-traces       : Generate keyboard's traces to be added to the kicad_pcb"
    echo "    help                  : Print this help dialog"
}

if [ "$action" = "generate-render" ]; then
    generate_render
elif [ "$action" = "generate-case" ]; then
    generate_case
elif [ "$action" = "generate-ponoko" ]; then
    generate_ponoko
elif [ "$action" = "generate-perimeters" ]; then
    generate_perimeters
elif [ "$action" = "generate-pcb" ]; then
    generate_pcb
elif [ "$action" = "generate-traces" ]; then
    generate_traces
elif [ "$action" = "help" ]; then
    print_usage
else
    print_usage
    exit 1
fi
