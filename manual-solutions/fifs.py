import asyncio

from starknet_py.contract import Contract
from starknet_py.net import AccountClient, KeyPair
from starknet_py.net.gateway_client import GatewayClient
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.networks import TESTNET
from starknet_py.net.signer.stark_curve_signer import StarkCurveSigner
from starkware.crypto.signature.signature import private_to_stark_key
from starkware.starknet.core.os.contract_address.contract_address import \
    calculate_contract_address_from_hash

testnet = "testnet"
chain_id = StarknetChainId.TESTNET


def felt_to_str(felt):
    length = (felt.bit_length() + 7) // 8
    return felt.to_bytes(length, byteorder="big").decode("utf-8")


async def run():

    rpc_endpoint = "http://6f6d549c-fc15-432c-bddd-5463b33cdd4f@127.0.0.1:5050"
    private_key = "0xfa15cfdb1a4b97a3c0ae05667d331907"
    player_address = int(
        "0x78aa70a8bc53fe835538f9198b0f40451c1c8132a056176f5eaf8a8844e6cc1", 16
    )
    contract = "0x10c512268b39e2f460569ccc019bab6ddd6066bc5f4136ac524ab1601accf69"
    gateway_client = GatewayClient(rpc_endpoint, TESTNET)

    for i in range(1, 22):
        print("Player", i)

        # Deploys an account on testnet and returns an instance
        account_client = await AccountClient.create_account(
            client=gateway_client, private_key=i, chain=StarknetChainId.TESTNET
        )

        c = await Contract.from_address(contract, account_client)

        result = await c.functions["claim"].invoke(max_fee=int(0))
        result = await result.wait_for_acceptance()

        result = await c.functions["get_balance"].call(account_client.address)
        print("Player", i, "balance", result)

    prvkey = int(private_key, 16)
    pubkey = private_to_stark_key(prvkey)
    key_pair = KeyPair(private_key=prvkey, public_key=pubkey)
    gateway_client = GatewayClient(rpc_endpoint, TESTNET)
    print("Player address", hex(player_address))

    signer = StarkCurveSigner(player_address, key_pair, StarknetChainId.TESTNET)
    account_client = AccountClient(
        client=gateway_client,
        address=player_address,
        signer=signer,
        supported_tx_version=1,
    )

    c = await Contract.from_address(contract, account_client)

    result = await c.functions["claim"].invoke(max_fee=int(1e16))
    await result.wait_for_acceptance()
    print("Claime res", result)
    result = await result.wait_for_acceptance()
    print("Claime res", result)

    balance = (await c.functions["get_balance"].call(account_client.address)).balance
    print("Balance", balance)
    supply = (await c.functions["get_total_supply"].call()).supply
    print("Supply", supply)


if __name__ == "__main__":
    asyncio.run(run())
