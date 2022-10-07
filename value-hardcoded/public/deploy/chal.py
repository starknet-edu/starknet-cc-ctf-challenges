import cairo_sandbox

from pathlib import Path

from starknet_py.net import AccountClient
from starknet_py.contract import Contract
from starkware.python.utils import to_bytes

async def deploy(client: AccountClient, player_address: int) -> int:
    print("[+] deploying value-hardcoded")
    value_deployment = await Contract.deploy(
        client=client,
        compiled_contract=Path("compiled/value-hardcoded.cairo").read_text(),
        constructor_args=[],
    )
    await value_deployment.wait_for_acceptance()

    return value_deployment.deployed_contract.address


async def checker(client: AccountClient, value_contract: Contract, player_address: int) -> bool:
    solution = (await value_contract.functions["is_challenge_done"].call()).res

    return solution == 1

cairo_sandbox.run_launcher([
    cairo_sandbox.new_launch_instance_action(deploy),
    cairo_sandbox.new_kill_instance_action(),
    cairo_sandbox.new_get_flag_action(checker),
])