%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.starknet.common.syscalls import get_caller_address

struct Token {
    token_address: felt,
    token_id: felt,
}

@storage_var
func balance() -> (res: felt) {
}

@storage_var
func owner() -> (res: Token) {
}

@external
func update_token{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    new_token: Token
) {
    owner.write(new_token);
    return ();
}

@external
func increase_balance{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    amount: felt
) {
    let (res) = balance.read();
    balance.write(res + amount);
    return ();
}

@view
func get_balance{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() -> (res: felt) {
    let (res) = balance.read();
    return (res,);
}
