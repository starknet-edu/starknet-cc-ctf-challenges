from paradigmctf.cairo_challenge import *

from starknet_py.net import AccountClient
from starknet_py.contract import Contract

from starkware.python.utils import from_bytes

async def solver(client: AccountClient, intro_contract: Contract):
    balance = (await intro_contract.functions["get_balance"].call()).res
    print("Balance", balance)

    diff = 31333333377 - balance
    print("Diff", diff)
    solution = diff
    for i in range (0, 14):
        if ((diff + i + balance) % 14) == 0:
            solution = diff + i
            break
    print("Solution", solution)


    first_call = await intro_contract.functions["increase_balance"].invoke(solution, max_fee=int(1e16))
    await first_call.wait_for_acceptance()
    second_call = await intro_contract.functions["solve_challenge"].invoke(max_fee=int(1e16))
    await second_call.wait_for_acceptance()

run_solver(solver)
