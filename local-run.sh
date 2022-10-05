#!/bin/bash

IMAGE="$1:latest"
PORT="$2"
HTTP_PORT="$3"

echo "[+] running challenge"
exec docker run \
    -e "PORT=$PORT" \
    -e "HTTP_PORT=$HTTP_PORT" \
    -e "ETH_RPC_URL=$ETH_RPC_URL" \
    -e "FLAG=PCTF{flag}" \
    -e "RLIMIT_CPU=600" \
    -p "$PORT:$PORT" \
    -p "$HTTP_PORT:$HTTP_PORT" \
    "$IMAGE"
