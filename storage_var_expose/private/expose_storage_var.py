#!/bin/python3
from starkware.starknet.public.abi import get_storage_var_address

password = get_storage_var_address('password')
print(f'password : {password}')