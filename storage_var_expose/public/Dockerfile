FROM amanusk/cairo-base:latest

COPY deploy/ /home/ctf/

COPY contracts /tmp/contracts

RUN true \
    && mkdir /home/ctf/compiled \
    && cd /tmp/contracts \
    && starknet-compile --debug_info_with_source storage_var_expose.cairo > /home/ctf/compiled/storage_var_expose.cairo \
    && rm -rf /tmp/contracts \
    && true
