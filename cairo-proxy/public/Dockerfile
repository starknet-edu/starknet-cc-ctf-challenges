FROM 0xaurelou/cairo-ctf-v0.10:latest

COPY deploy/ /home/ctf/

COPY contracts /tmp/contracts

RUN mkdir /home/ctf/compiled \
    && cd /tmp/contracts \
    && starknet-compile --debug_info_with_source almost_erc20.cairo > /home/ctf/compiled/almost_erc20.cairo \
    && starknet-compile --debug_info_with_source proxy.cairo > /home/ctf/compiled/proxy.cairo \
    && rm -rf /tmp/contracts \
    && true
