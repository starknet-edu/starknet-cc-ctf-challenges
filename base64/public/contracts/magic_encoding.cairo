%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin, BitwiseBuiltin
from starkware.cairo.common.alloc import alloc

from base64 import magic_encode

@storage_var
func challenge_is_done() -> (res: felt) {
}

@view
func is_challenge_done {syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr : felt }() -> (res: felt) {
    let (res : felt) = challenge_is_done.read();
    return(res,);
}

@view
func test_password{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, bitwise_ptr: BitwiseBuiltin*, range_check_ptr}(password: felt) -> (){
    alloc_locals;
    let (array : felt*) = alloc();
    assert [array] = password;
    let (_,result) = magic_encode(1,array);
    let check : felt = [result];
    if (check == 120083678913207725988082986712944560747) {
        challenge_is_done.write(1);
        return ();
    }

    return ();
}