from starknet_py.net.gateway_client import GatewayClient
from starknet_py.contract import Contract
from starknet_py.net.networks import TESTNET
from starknet_py.net.models import StarknetChainId

client = GatewayClient(TESTNET)
counter = 0
last_block = 0

while True:
    block = client.get_block_sync(block_number="latest")
    print(f'Actual block is {block.block_number}')
    if block.block_number % 5 == 0 and block.block_number != last_block:
        counter += 1
        last_block = block.block_number
        print(f'Counter is now equal to {counter}')
    if counter == 5 :
        print('Counter is equal to 5')
        break

print("SOLVED")