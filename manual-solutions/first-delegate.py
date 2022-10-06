
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
    uuid="eefe1065-8cc7-4eaa-b0d7-a49c171761c4"
    rpc_endpoint="http://eefe1065-8cc7-4eaa-b0d7-a49c171761c4@127.0.0.1:5050"
    private_key="0x7e1ae2e2d0bdb8c93c5aaf4aa5d62a1b"
    player_address="2711595295135484177887488099585152921339400029065313438182185814610828186983"
    contract=("0x14cac5ee286bbe2cfa5ecf4f33a391c2325ff32a0aeac54345a28ab2fb195fd")

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
    result = c.functions["test_password"].invoke_sync(314159265359, max_fee=0)
    print("After solve call")
    result = c.functions["is_challenge_done"].call_sync()
    print(result)
    if getattr(result,"bool")  == 1:
        print("SOLVED !")
    else:
        print("Try again you didn't find the solution")

    # TO CHANGE