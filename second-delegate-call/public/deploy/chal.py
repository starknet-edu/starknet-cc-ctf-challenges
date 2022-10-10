import cairo_sandbox

from pathlib import Path

from starknet_py.net import AccountClient
from starknet_py.contract import Contract
from starkware.python.utils import to_bytes

async def deploy(client: AccountClient, player_address: int) -> int:
    print("[+] deploying proxy-second-delegate")
    proxy_deployment = await Contract.deploy(
        client=client,
        compiled_contract=Path("compiled/proxy-second.cairo").read_text(),
        constructor_args=[],
    )
    class_hash = await client.get_class_hash_at(hex(proxy_deployment.deployed_contract.address))
    print(f'✨ Contract deployed at {hex(proxy_deployment.deployed_contract.address)}')
    await proxy_deployment.wait_for_acceptance()

    print("[+] deploying second-delegate")
    second_deployment = await Contract.deploy(
        client=client,
        compiled_contract=Path("compiled/second.cairo").read_text(),
        constructor_args=[class_hash],
    )
    await second_deployment.wait_for_acceptance()

    return (second_deployment.deployed_contract.address)


async def checker(client: AccountClient, riddle_contract: Contract, player_address: int) -> bool:
    solution = (await riddle_contract.functions["is_challenge_done"].call()).res
    return solution == 1

cairo_sandbox.run_launcher([
    cairo_sandbox.new_launch_instance_action(deploy),
    cairo_sandbox.new_kill_instance_action(),
    cairo_sandbox.new_get_flag_action(checker),
])