import asyncio
from pathlib import Path

from starknet_py.contract import Contract
from starknet_py.net import AccountClient, KeyPair
from starknet_py.net.gateway_client import GatewayClient
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.networks import MAINNET, TESTNET
from starknet_py.net.signer.stark_curve_signer import StarkCurveSigner
from starkware.python.utils import to_bytes
from starkware.starknet.core.os.contract_address.contract_address import \
    calculate_contract_address_from_hash

MAX_LEN_FELT = 31
testnet = "testnet"
chain_id = StarknetChainId.TESTNET


def str_to_felt(text):
    if len(text) > MAX_LEN_FELT:
        raise Exception("Text length too long to convert to felt.")

    return int.from_bytes(text.encode(), "big")


async def main():
    node_url = "http://3a666138-b77a-4251-9e73-4896f7e05a6c@127.0.0.1:5050"
    contractAddress = (
        "0x2377325ddc7575c83eb51d2b223b53b9a834726d26c4a72f2f4aaf1a8f881b1"
    )
    private_key = "0xf23a838c17900bb04f8337c3cbc40ef3"
    player_address = 1061187669397351790558506865006261457388527257759064434023491866176219505681

    gateway_client = GatewayClient(node_url, TESTNET)

    key_pair = KeyPair.from_private_key(key=int(private_key, 16))
    print(key_pair)

    player_public_key = key_pair.public_key
    print("Player public key", player_public_key)

    # player_address = calculate_contract_address_from_hash(
    #     salt=20,
    #     class_hash=1803505466663265559571280894381905521939782500874858933595227108099796801620,
    #     constructor_calldata=[player_public_key],
    #     deployer_address=0,
    # )
    # print("Player address", player_address, hex(player_address))

    signer = StarkCurveSigner(player_address, key_pair, StarknetChainId.TESTNET)
    account_client = AccountClient(
        client=gateway_client,
        address=player_address,
        signer=signer,
        supported_tx_version=1,
    )

    riddle_contract = Contract(
        address=contractAddress, abi=riddleABI, client=account_client
    )
    solution = (await riddle_contract.functions["solution"].call()).solution
    print("Current solution", solution)

    input_string = str_to_felt("man")
    response = await account_client.execute(
        calls=[riddle_contract.functions["solve"].prepare(input_string)],
        max_fee=int(1e16),
    )
    status = await account_client.wait_for_tx(response.transaction_hash)
    print(status)
    print(response)

    solution = (await riddle_contract.functions["solution"].call()).solution

    print("New solution", solution)
    if to_bytes(solution).lstrip(b"\x00") == b"man":
        print("SOLVED!")


riddleABI = [
    {
        "inputs": [{"name": "solution", "type": "felt"}],
        "name": "solve",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [],
        "name": "solution",
        "outputs": [{"name": "solution", "type": "felt"}],
        "stateMutability": "view",
        "type": "function",
    },
]


if __name__ == "__main__":
    asyncio.run(main())
