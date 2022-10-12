from paradigmctf.cairo_challenge import *

from starknet_py.net import AccountClient
from starknet_py.contract import Contract

from starkware.python.utils import from_bytes

async def solver(client: AccountClient, riddle_contract: Contract):
    result = await riddle_contract.functions["test_password"].invoke([65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 67, 67, 65, 65, 65, 65], max_fee=int(1e16))
    await result.wait_for_acceptance()

run_solver(solver)