FROM amanusk/cairo-base:latest

COPY deploy/ /home/ctf/

COPY contracts /tmp/contracts

RUN true \
    && mkdir /home/ctf/compiled \
    && cd /tmp/contracts \
    && cat call-hardcoded.json > /home/ctf/compiled/call-hardcoded.json \
    && rm -rf /tmp/contracts \
    && true
