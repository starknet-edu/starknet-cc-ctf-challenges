FROM amanusk/cairo-base:latest

COPY deploy/ /home/ctf/

COPY contracts /tmp/contracts

RUN true \
    && mkdir /home/ctf/compiled \
    && cd /tmp/contracts \
    && cat bitwise-xor.json > /home/ctf/compiled/bitwise-xor.json \
    && rm -rf /tmp/contracts \
    && true
