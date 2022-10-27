#!/bin/bash


imgs=(
    "base"
    "cairo-base"
    "magic-encoding"
    "account-obstruction"
    "unique-id"
    "cairo-bid"
    "dna"
    "cairo-intro"
    "first-come-first-served"
    "claim-a-punk"
)

for img in "${imgs[@]}"; do
    aws ecr batch-delete-image --repository-name starkware-ctf/$img --image-ids imageTag=latest
done
