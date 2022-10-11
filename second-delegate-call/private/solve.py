from paradigmctf.cairo_challenge import *

from starknet_py.net import AccountClient
from starknet_py.contract import Contract

from starkware.python.utils import from_bytes

async def solver(client: AccountClient, riddle_contract: Contract):
    result = await riddle_contract.functions["test_my_password"].invoke(1515, max_fee=int(1e16))
    await result.wait_for_acceptance()

run_solver(solver)