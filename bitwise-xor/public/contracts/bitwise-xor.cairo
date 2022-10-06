%lang starknet

from starkware.cairo.common.cairo_builtins import BitwiseBuiltin
from starkware.cairo.common.bitwise import bitwise_xor
from starkware.cairo.common.cairo_builtins import HashBuiltin

@storage_var
func challenge_is_done() -> (res: felt) {
}

@view
func is_challenge_done{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr : felt } () -> (res: felt) {
    let (res) = challenge_is_done.read();
    return(res,);
}

@external
func test_password{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr :felt, bitwise_ptr : BitwiseBuiltin*}(password : felt) -> (res : felt){
    let (result) = bitwise_xor(12345, password);
    if (result == 19423) {
        challenge_is_done.write(1);
        return (res= 1);
    }
    return (res= 0);
}