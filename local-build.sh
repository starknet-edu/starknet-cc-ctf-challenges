#!/bin/bash

set -euo pipefail

build_challenge() {
    name="$1"
    echo "building $name"

    tag="$name:latest"

    docker buildx build --platform linux/amd64 -t "$tag" "$name/public"
}

declare -a chals=(
    "block-number"
)

for chal in "${chals[@]}"; do
    build_challenge $chal
done
