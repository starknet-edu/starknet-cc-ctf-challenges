# First compile the exploit contract
# starknet-compile exploit.cairo --output exploit.json

from pathlib import Path

from starknet_py.contract import Contract
from starknet_py.net import AccountClient
from starkware.starknet.core.os.contract_address.contract_address import \
    calculate_contract_address_from_hash
from starkware.starknet.public.abi import get_storage_var_address

from paradigmctf.cairo_challenge import *


async def solver(client: AccountClient, puzzle_contract: Contract):

    # impl_1_class_hash = await client.get_storage_at(
    #     puzzle_contract.address, get_storage_var_address("class_hash"), "latest"
    # )

    # impl_2_address = await client.get_storage_at(
    #     puzzle_contract.address, get_storage_var_address("implementation_hash"), "latest"
    # )

    print("Client address", client.address)
    value = int(12345) + int(3609145100) + int(client.address)

    result = await puzzle_contract.functions["solve_step_1"].invoke(
        value, max_fee=int(1e16)
    )
    await result.wait_for_acceptance()

    step_1 = await client.get_storage_at(
        puzzle_contract.address, get_storage_var_address("step_1_done"), "latest"
    )
    print("Step 1", step_1)

    value = int(965647271) + int(1010886179) + int(puzzle_contract.address)
    result = await puzzle_contract.functions["solve_step_2"].invoke(
        value, max_fee=int(1e16)
    )
    await result.wait_for_acceptance()

    step_2 = await client.get_storage_at(
        puzzle_contract.address, get_storage_var_address("step_2_done"), "latest"
    )
    print("Step 2", step_2)

    value = 373968 
    result = await puzzle_contract.functions["solve_step_3"].invoke(
        value, max_fee=int(1e16)
    )
    await result.wait_for_acceptance()

    step_3 = await client.get_storage_at(
        puzzle_contract.address, get_storage_var_address("step_3_done"), "latest"
    )
    print("Step 3", step_3)

    value = 84092830 
    result = await puzzle_contract.functions["solve_step_4"].invoke(
        value, max_fee=int(1e16)
    )
    await result.wait_for_acceptance()

    step_4 = await client.get_storage_at(
        puzzle_contract.address, get_storage_var_address("step_4_done"), "latest"
    )
    print("Step 4", step_4)

    result = await puzzle_contract.functions["solve"].invoke(
        max_fee=int(1e16)
    )
    await result.wait_for_acceptance()


run_solver(solver)
