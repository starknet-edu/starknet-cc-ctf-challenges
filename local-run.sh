#!/bin/bash

IMAGE="$1:latest"
PORT="$2"
HTTP_PORT="$3"

FLAG=`cat $1/info.yaml | grep flag | cut -f 2 -d " " | sed 's/\"//g'`

echo "[+] running challenge"
exec docker run \
    -e "PORT=$PORT" \
    -e "HTTP_PORT=$HTTP_PORT" \
    -e "ETH_RPC_URL=$ETH_RPC_URL" \
    -e "FLAG=$FLAG" \
    -e "RLIMIT_CPU=600" \
    -p "$PORT:$PORT" \
    -p "$HTTP_PORT:$HTTP_PORT" \
    "$IMAGE"
