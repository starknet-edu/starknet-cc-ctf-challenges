#!/bin/bash

set -euo pipefail

build_challenge() {
    name="$1"
    echo "building $name"

    tag="801546505238.dkr.ecr.eu-central-1.amazonaws.com/starkware-ctf/$name:latest"

    docker buildx build --platform linux/amd64 --push -t "$tag" "$name/public"
    #docker build -t "$tag" "$name/public" &
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
)

docker pull 801546505238.dkr.ecr.eu-central-1.amazonaws.com/starkware-ctf/cairo-base:latest

for chal in "${chals[@]}"; do
    build_challenge $chal
done
