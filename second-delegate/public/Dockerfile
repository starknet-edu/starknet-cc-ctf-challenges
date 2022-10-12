FROM amanusk/cairo-base:latest

COPY deploy/ /home/ctf/

COPY contracts /tmp/contracts

RUN true \
    && mkdir /home/ctf/compiled \
    && cd /tmp/contracts \
    && starknet-compile --debug_info_with_source proxy-second.cairo > /home/ctf/compiled/proxy-second.cairo \
    && starknet-compile --debug_info_with_source second.cairo > /home/ctf/compiled/second.cairo \
    && rm -rf /tmp/contracts \
    && true
