from paradigmctf.cairo_challenge import *

from starknet_py.net import AccountClient
from starknet_py.contract import Contract

from starkware.python.utils import from_bytes

async def solver(client: AccountClient, storage_contract: Contract):
    result = await storage_contract.functions["test_password"].invoke(991928, max_fee=int(1e16))
    await result.wait_for_acceptance()

run_solver(solver)