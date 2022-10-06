%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin

@storage_var
func real_password() -> (res: felt) {
}

@constructor
func constructor{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(password : felt){
    real_password.write(password);
    return ();
}

@view
func get_password {syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr} () -> (password : felt){
    let (password) = real_password.read();
    return(password,);
}


@view
func test_password{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr} (password : felt) -> (res : felt){
    let (real_password_ : felt) = real_password.read();
    if (real_password_ == password){
        return (res= 1);
    }
    return (res= 0);
}