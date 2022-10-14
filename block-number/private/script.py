from starknet_py.net.gateway_client import GatewayClient
from starknet_py.contract import Contract
from starknet_py.net.networks import TESTNET
from starknet_py.net.models import StarknetChainId

client = GatewayClient(TESTNET)
counter = 0

block = client.get_block_sync()
print(f"Block number{block.block_number}")