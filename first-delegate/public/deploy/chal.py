
import cairo_sandbox

from pathlib import Path

from starknet_py.net import AccountClient
from starknet_py.contract import Contract
from starkware.python.utils import to_bytes

async def deploy(client: AccountClient, player_address: int) -> int:
    print("[+] deploying proxy-first")
    proxy_deployment = await Contract.deploy(
        client=client,
        compiled_contract=Path("compiled/proxy-first.json").read_text(),
        constructor_args=[680],
    )
    await proxy_deployment.wait_for_acceptance()

    print("[+] deploying first-delegate")
    first_deployement= await Contract.deploy(
        client=client,
        compiled_contract=Path("compiled/first-delegate.json").read_text(),
        constructor_args=[proxy_deployment.deployed_contract.address],
    )
    await first_deployement.wait_for_acceptance()
    return (first_deployement.deployed_contract.address)


async def checker(client: AccountClient, first_contract: Contract, player_address: int) -> bool:
    solution = (await first_contract.functions["is_challenge_done"].call()).bool

    return solution == 1


cairo_sandbox.run_launcher([
    cairo_sandbox.new_launch_instance_action(deploy),
    cairo_sandbox.new_kill_instance_action(),
    cairo_sandbox.new_get_flag_action(checker),
])