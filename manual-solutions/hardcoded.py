
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
    uuid="378542da-4f53-48f5-846a-2a1ac13f0eb9"
    rpc_endpoint="http://378542da-4f53-48f5-846a-2a1ac13f0eb9@127.0.0.1:5050"
    private_key="0xa4c3234f8e7f13cdb21fe70802dcaa75"
    player_address="1241110535188280126858073401387392131399892228675729763341753052341486221210"
    contract=("0x1c1566ff52a986036b45a67675051aa477ad6dcbe94864e5df07a7d5594086b")

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
    password = c.functions["get_password"].call_sync()
    print(password)
    password = getattr(password, "password")
    c.functions["test_password"].invoke_sync(password, max_fee=0)
    result = c.functions["is_challenge_done"].call_sync()
    print("After solve call")
    print(result)
    if getattr(result, "res") == 1:
        print("SOLVED !")
    else:
        print("Try again you didn't find the solution")

    # TO CHANGE