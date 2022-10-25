from paradigmctf.cairo_challenge import *

from starknet_py.net import AccountClient
from starknet_py.contract import Contract

from starkware.python.utils import from_bytes

async def solver(client: AccountClient, intro_contract: Contract):
    first_call = await intro_contract.functions["increase_balance"].invoke(42, max_fee=int(1e16))
    await first_call.wait_for_acceptance()
    second_call = await intro_contract.functions["solve_challenge"].invoke(max_fee=int(1e16))
    await second_call.wait_for_acceptance()

run_solver(solver)
