#!/bin/python3
from starkware.starknet.public.abi import get_storage_var_address

def hex_to_felt(val):
    return int(val,16);