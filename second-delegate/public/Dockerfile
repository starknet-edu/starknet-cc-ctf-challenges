FROM amanusk/cairo-base:latest

COPY deploy/ /home/ctf/

COPY contracts /tmp/contracts

RUN true \
    && mkdir /home/ctf/compiled \
    && cd /tmp/contracts \
    && cat proxy-second.json > /home/ctf/compiled/proxy-second.json \
    && cat second.json > /home/ctf/compiled/second.json \
    && rm -rf /tmp/contracts \
    && true
