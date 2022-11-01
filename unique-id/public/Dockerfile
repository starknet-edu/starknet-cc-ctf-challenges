FROM 801546505238.dkr.ecr.eu-central-1.amazonaws.com/starkware-ctf/cairo-base:latest

COPY deploy/ /home/ctf/

COPY contracts /tmp/contracts

RUN true \
    && mkdir /home/ctf/compiled \
    && cd /tmp/contracts \
    && starknet-compile --debug_info_with_source implementation_v1.cairo > /home/ctf/compiled/implementation_v1.json \
    && starknet-compile --debug_info_with_source proxy.cairo > /home/ctf/compiled/proxy.json \
    && rm -rf /tmp/contracts \
    && true
