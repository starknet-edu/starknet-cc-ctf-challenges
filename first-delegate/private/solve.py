from paradigmctf.cairo_challenge import *

from starknet_py.net import AccountClient
from starknet_py.contract import Contract

from starkware.starknet.public.abi import get_storage_var_address
from starkware.starknet.core.os.contract_address.contract_address import calculate_contract_address_from_hash


async def solver(client: AccountClient, bitwise_contract: Contract):
    result = await bitwise_contract.functions["test_password"].invoke(314159265359, max_fee=int(1e16))
    await result.wait_for_acceptance()

run_solver(solver)