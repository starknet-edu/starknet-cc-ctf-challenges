%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin

@storage_var
func challenge_is_done() -> (res: felt) {
}

const real_password = 1618033988749;

@view
func is_challenge_done{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}() -> (res : felt){
    let (res : felt) = challenge_is_done.read();
    return(res,);
}

@external
func test_password{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(password : felt) -> (){
    if (real_password == password){
        challenge_is_done.write(1);
        return ();
    }
    return ();
}
