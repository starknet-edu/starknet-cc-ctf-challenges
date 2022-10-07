import cairo_sandbox

from pathlib import Path

from starknet_py.net import AccountClient
from starknet_py.contract import Contract
from starkware.python.utils import to_bytes

OWNER = 0x1234567890123456789012345678901234567890

async def deploy(client: AccountClient, player_address: int) -> int:
    print("[+] deploying hardcoded")
    riddle_deployment = await Contract.deploy(
        client=client,
        compiled_contract=Path("compiled/hardcoded.cairo").read_text(),
        constructor_args=[592965625081988036501471237208223793],
    )
    await riddle_deployment.wait_for_acceptance()

    return riddle_deployment.deployed_contract.address


async def checker(client: AccountClient, hardcoded_contract: Contract, player_address: int) -> bool:
    result = (await hardcoded_contract.functions["is_challenge_done"].call()).res

    return result == 1

cairo_sandbox.run_launcher([
    cairo_sandbox.new_launch_instance_action(deploy),
    cairo_sandbox.new_kill_instance_action(),
    cairo_sandbox.new_get_flag_action(checker),
])