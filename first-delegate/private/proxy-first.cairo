%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin

@storage_var
func password() -> (res: felt) {
}

@constructor
func constructor{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(pass : felt) {
    password.write(pass + 15);
    return();
}

@view
func test_password{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(_password : felt) -> (res : felt){
    let (real_password_ : felt) = password.read();
    if (real_password_ == _password){
        return (res= 1);
    }
    return (res= 0);
} 