import cairo_sandbox

from pathlib import Path

from starknet_py.net import AccountClient
from starknet_py.contract import Contract
from starkware.python.utils import from_bytes

async def deploy(client: AccountClient, player_address: int) -> int:
    print("[+] implementation_v0")
    implementation_v0_deployment = await Contract.deploy(
        client=client,
        compiled_contract=Path("compiled/implementation_v0.json").read_text(),
        constructor_args=[
        ],
    )
    await implementation_v0_deployment.wait_for_acceptance()

    print("[+] deploying proxy")
    proxy_deployment = await Contract.deploy(
        client=client,
        compiled_contract=Path("compiled/proxy.json").read_text(),
        constructor_args=[
            await client.get_class_hash_at(implementation_v0_deployment.deployed_contract.address),
            client.address,
        ],
    )
    await proxy_deployment.wait_for_acceptance()

    print("[+] deploying upgrade")
    implementation_v1_deployment = await Contract.deploy(
        client=client,
        compiled_contract=Path("compiled/implementation_v1.json").read_text(),
        constructor_args=[
        ],
        salt=111111,
    )
    await implementation_v1_deployment.wait_for_acceptance()


    print("[+] Upgrading implementation")
    response = await client.execute(
        calls=[
            proxy_deployment.deployed_contract.functions["upgrade"].prepare(await client.get_class_hash_at(implementation_v1_deployment.deployed_contract.address)),
        ],
        max_fee=int(1e16)
    )
    await client.wait_for_tx(response.transaction_hash)

    return proxy_deployment.deployed_contract.address



async def checker(client: AccountClient, proxy_contract: Contract, player_address: int) -> bool:
    current_owner = (await proxy_contract.functions["get_owner"].call()).curr_owner

    return current_owner == player_address

cairo_sandbox.run_launcher([
    cairo_sandbox.new_launch_instance_action(deploy),
    cairo_sandbox.new_kill_instance_action(),
    cairo_sandbox.new_get_flag_action(checker),
])
