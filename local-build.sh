#!/bin/bash

set -euo pipefail

build_challenge() {
    name="$1"
    echo "building $name"

    tag="$name:latest"

    docker buildx build --platform linux/amd64 -t "$tag" "$name/public"
}

declare -a chals=(
    # "cairo-intro"
    "riddle-of-the-sphinx"
    "cairo-auction"
)

for chal in "${chals[@]}"; do
    build_challenge $chal
done
