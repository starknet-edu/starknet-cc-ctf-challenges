FROM amanusk/cairo-base:latest

COPY deploy/ /home/ctf/

COPY contracts /tmp/contracts

RUN true \
    && mkdir /home/ctf/compiled \
    && cd /tmp/contracts \
    && cat find-value.json > /home/ctf/compiled/find-value.json \
    && rm -rf /tmp/contracts \
    && true
