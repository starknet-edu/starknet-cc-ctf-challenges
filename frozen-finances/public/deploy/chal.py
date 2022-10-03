import cairo_sandbox

from pathlib import Path

from starknet_py.net import AccountClient
from starknet_py.contract import Contract
from starkware.python.utils import from_bytes

async def deploy(client: AccountClient, player_address: int) -> int:
    print("[+] deploying frozen account")
    frozen_deployment = await Contract.deploy(
        client=client,
        compiled_contract=Path("compiled/frozen.cairo").read_text(),
        constructor_args=[],
    )
    await frozen_deployment.wait_for_acceptance()

async def checker(client: AccountClient, frozen_contract: Contract, player_address: int) -> bool:
    balance = (await auction_contract.balance["current_winner"].call())

    return balance == 0

cairo_sandbox.run_launcher([
    cairo_sandbox.new_launch_instance_action(deploy),
    cairo_sandbox.new_kill_instance_action(),
    cairo_sandbox.new_get_flag_action(checker),
])

