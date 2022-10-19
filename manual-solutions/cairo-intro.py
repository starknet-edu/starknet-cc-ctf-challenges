from starknet_py.contract import Contract
from starknet_py.net import AccountClient, KeyPair
from starknet_py.net.gateway_client import GatewayClient
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.networks import TESTNET
from starknet_py.net.signer.stark_curve_signer import StarkCurveSigner
from starkware.starknet.core.os.contract_address.contract_address import \
    calculate_contract_address_from_hash
from starkware.crypto.signature.signature import private_to_stark_key

testnet = "testnet"
chain_id = StarknetChainId.TESTNET

if __name__ == "__main__":
   
    # TO CHANGE /*

    # Update your info after running ./run.sh cairo-intro 31337 5050 in a terminal (don't shutdown it)
    # And in an another terminal do nc localhost 31137, this will show you an interface, press 1, 1.
    # This will show you can all the variable use in this contract, copy paste them here.
    uuid="83105a03-9da8-4826-aff6-8a0c6776768e"
    rpc_endpoint="http://83105a03-9da8-4826-aff6-8a0c6776768e@127.0.0.1:5050"
    private_key="0x83753b1660199e4ccdd69b4ff698301"
    player_address="3448323533803714245552402473325308817396493025463700460697268229833976791785"
    contract=("0x6985812cfe5ff790aa87b31585a948947f87fb6b8a1e666e8e37a5b93281ee9")

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
    print("Player address", hex(player_address))

    signer = StarkCurveSigner(player_address, key_pair, StarknetChainId.TESTNET)
    account_client = AccountClient(
        client=gateway_client,
        address=player_address,
        signer=signer,
        supported_tx_version=1,
    )

    intro_contract = Contract.from_address_sync(contract, account_client)

    challenge_status = intro_contract.functions["is_challenge_done"].call_sync()
    print("Challenge is done : ", challenge_status)

    print("Increase balance")
    intro_contract.functions["increase_balance"].invoke_sync(42, max_fee=0)

    intro_contract.functions["challenge_passed"].invoke_sync(max_fee=0)
    
    challenge_status = intro_contract.functions["is_challenge_done"].call_sync()
    print("Challenge is done : ", challenge_status)

    if getattr(challenge_status,"id") == 1:
        print("SOLVED!")