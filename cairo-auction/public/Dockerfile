FROM 801546505238.dkr.ecr.eu-central-1.amazonaws.com/starkware-ctf/cairo-base:latest

COPY deploy/ /home/ctf/

COPY contracts /tmp/contracts

RUN true \
    && mkdir /home/ctf/compiled \
    && cd /tmp/contracts \
    && starknet-compile --debug_info_with_source auction.cairo > /home/ctf/compiled/auction.cairo \
    && starknet-compile --debug_info_with_source openzeppelin/token/erc20/presets/ERC20.cairo > /home/ctf/compiled/erc20.cairo \
    && rm -rf /tmp/contracts \
    && true
