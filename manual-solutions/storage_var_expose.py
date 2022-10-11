
from starknet_py.contract import Contract
from starknet_py.net import AccountClient, KeyPair
from starknet_py.net.gateway_client import GatewayClient
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.networks import TESTNET
from starknet_py.net.signer.stark_curve_signer import StarkCurveSigner
from starkware.starknet.core.os.contract_address.contract_address import \
    calculate_contract_address_from_hash
from starkware.crypto.signature.signature import private_to_stark_key

def felt_to_str(felt):
    length = (felt.bit_length() + 7) // 8
    return felt.to_bytes(length, byteorder="big").decode("utf-8")

if __name__ == "__main__":

    # TO CHANGE /*

    # Update your info after running ./run.sh riddle-of-sphinx 31337 5050 in a terminal (don't shutdown it)
    # And in an another terminal do nc localhost 31137, this will show you an interface, press 1, 1.
    # This will show you can all the variable use in this contract, copy paste them here.
    uuid="7e0f7eab-45b1-45c7-b9fe-7db4124b4d84"
    rpc_endpoint="http://7e0f7eab-45b1-45c7-b9fe-7db4124b4d84@127.0.0.1:5050"
    private_key="0x9410cb6fe01156d90edbfe7d8f804f65"
    player_address="211679800863780364536285702014718968154264489409253250162983277240541332224"
    contract=("0x1992a907fb47d5c0303001327a7e8f0b3e5eae288a7099c98b447af57bfbe6")

    # TO CHANGE */

    prvkey=int(private_key, 16)
    pubkey=private_to_stark_key(prvkey)
    key_pair=KeyPair(private_key=prvkey, public_key=pubkey)
    player_address=calculate_contract_address_from_hash(
        salt=20,
        class_hash=1803505466663265559571280894381905521939782500874858933595227108099796801620,
        constructor_calldata=[pubkey],
        deployer_address=0
    )

    gateway_client = GatewayClient(rpc_endpoint, TESTNET)
    print("Player address", player_address, hex(player_address))

    signer = StarkCurveSigner(player_address, key_pair, StarknetChainId.TESTNET)
    account_client = AccountClient(
        client=gateway_client,
        address=player_address,
        signer=signer,
        supported_tx_version=1,
    )

    c = Contract.from_address_sync(contract, account_client)

    # TO CHANGE /*

    # Solution for your exercise log it as you want 

    print("Before solve call")
    print(c.functions["is_challenge_done"].call_sync())
    c.functions["test_password"].invoke_sync(991928, max_fee=0)
    result = c.functions["is_challenge_done"].call_sync()
    print("After solve call")
    print(result)
    if getattr(result,"res") == 1:
        print("SOLVED !")
    else:
        print("Try again you didn't find the solution")

    # TO CHANGE