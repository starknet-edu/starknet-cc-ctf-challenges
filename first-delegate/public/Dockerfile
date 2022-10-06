FROM amanusk/cairo-base:latest

COPY deploy/ /home/ctf/

COPY contracts /tmp/contracts

RUN true \
    && mkdir /home/ctf/compiled \
    && cd /tmp/contracts \
    && starknet-compile --debug_info_with_source proxy-first.cairo > /home/ctf/compiled/proxy-first.cairo \
    && starknet-compile --debug_info_with_source first-delegate.cairo > /home/ctf/compiled/first-delegate.cairo \
    && rm -rf /tmp/contracts \
    && true
