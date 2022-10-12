from paradigmctf.cairo_challenge import *

from starknet_py.net import AccountClient
from starknet_py.contract import Contract

from starkware.python.utils import from_bytes

async def solver(client: AccountClient, harcoded_contract: Contract):
    result = await harcoded_contract.functions["test_password"].invoke(1618033988749, max_fee=int(1e16))
    await result.wait_for_acceptance()

run_solver(solver)
