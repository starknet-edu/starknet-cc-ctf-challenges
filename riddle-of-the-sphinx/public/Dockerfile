FROM 0xaurelou/cairo-ctf-v0.10:latest

COPY deploy/ /home/ctf/

COPY contracts /tmp/contracts

RUN mkdir /home/ctf/compiled \
    && cd /tmp/contracts \
    && starknet-compile --debug_info_with_source riddle.cairo > /home/ctf/compiled/riddle.cairo \
    && rm -rf /tmp/contracts \
    && true