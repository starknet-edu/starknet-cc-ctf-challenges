#!/bin/bash


imgs=(
    "base"
    "cairo-base"
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
)

for img in "${imgs[@]}"; do
    aws ecr batch-delete-image --repository-name starkware-ctf/$img --image-ids imageTag=latest
done
