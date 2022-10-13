FROM amanusk/cairo-base:latest

COPY deploy/ /home/ctf/

COPY contracts /tmp/contracts

RUN true \
    && mkdir /home/ctf/compiled \
    && cd /tmp/contracts \
    && starknet-compile --debug_info_with_source sha256.cairo > /home/ctf/compiled/sha256.cairo \
    && rm -rf /tmp/contracts \
    && true
