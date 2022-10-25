#!/bin/bash

set -euo pipefail

build_challenge() {
    name="$1"
    echo "building $name"

    tag="$name:latest"

    docker buildx build --platform linux/amd64 -t "$tag" "$name/public"
}

declare -a chals=(
    "magic-encoding"
    "account-obstruction"
    "unique-id"
    "cairo-bid"
    "dna"
    "cairo-intro"
    "claim-a-punk"
)

for chal in "${chals[@]}"; do
    build_challenge $chal
done
