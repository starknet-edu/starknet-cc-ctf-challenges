#!/bin/bash


chals=(
    "magic-encoding"
    "account-obstruction"
    "unique-id"
    "cairo-bid"
    "dna"
    "cairo-intro"
    "first-come-first-served"
    "claim-a-punk"
)


CHALLENGE_PORT=31300
CHALLENGE_HTTP_PORT=5050

export IMAGE=801546505238.dkr.ecr.eu-central-1.amazonaws.com/starkware-ctf
export RLIMIT_CPU=60
export PUBLIC_IP=192.168.5.12
export ENV=dddev


envsubst < docker-compose.yaml.header > docker-compose.yaml

for CHALLENGE_NAME in ${chals[@]} ; do
    echo "Generating $CHALLENGE_NAME"
    export CHALLENGE_FLAG=`cat ./$CHALLENGE_NAME/info.yaml | grep flag | cut -f 2 -d " " | sed 's/\"//g'`
    export CHALLENGE_NAME
    export CHALLENGE_PORT
    export CHALLENGE_HTTP_PORT
    envsubst < docker-compose.yaml.service >> docker-compose.yaml
    CHALLENGE_PORT=$((CHALLENGE_PORT+1))
    CHALLENGE_HTTP_PORT=$((CHALLENGE_HTTP_PORT+1))
done