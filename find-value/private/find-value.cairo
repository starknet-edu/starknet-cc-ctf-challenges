%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin

@storage_var
func real_password() -> (res: felt) {
}

@storage_var
func challenge_is_done() -> (res: felt) {
}

@constructor
func constructor{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(password : felt){
    let new_password : felt = password * 12;
    real_password.write(new_password);
    return ();
}

@view
func is_challenge_done{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr} () -> (res : felt){
    let (bool :felt) = challenge_is_done.read();
    return (bool,);
}

@view
func get_password {syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr} () -> (password : felt){
    let (password) = real_password.read();
    return(password,);
}

@external
func test_password{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr} (password : felt) -> (){
    let (real_password_ : felt) = real_password.read();
    if (real_password_ == password){
        challenge_is_done.write(1);
        return();
    }
    return ();
}