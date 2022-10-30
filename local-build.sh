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
    "access-denied"
    "dna"
    "cairo-intro"
    "frozen-finances"
    "first-come-first-served"
    "claim-a-punk"
    "puzzle-box"
    "solve-me"
)

for chal in "${chals[@]}"; do
    build_challenge $chal
done
