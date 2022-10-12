FROM amanusk/cairo-base:latest

COPY deploy/ /home/ctf/

COPY contracts /tmp/contracts

RUN true \
    && mkdir /home/ctf/compiled \
    && cd /tmp/contracts \
    && starknet-compile --debug_info_with_source call-hardcoded.cairo > /home/ctf/compiled/call-hardcoded.cairo \
    && rm -rf /tmp/contracts \
    && true
