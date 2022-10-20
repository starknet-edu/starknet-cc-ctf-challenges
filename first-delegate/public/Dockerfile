FROM amanusk/cairo-base:latest

COPY deploy/ /home/ctf/

COPY contracts /tmp/contracts

RUN true \
    && mkdir /home/ctf/compiled \
    && cd /tmp/contracts \
    && cat proxy-first.json > /home/ctf/compiled/proxy-first.json\
    && cat first-delegate.json > /home/ctf/compiled/first-delegate.json\
    && rm -rf /tmp/contracts \
    && true
