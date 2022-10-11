%lang starknet

from second import ITest_Password_Contract

from starkware.cairo.common.cairo_builtins import HashBuiltin

@storage_var
func class_hash() -> (res: felt) {
}

@storage_var
func challenge_is_done() -> (res : felt) {
}

@storage_var
func password() -> (res : felt){
}

@constructor
func constructor{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr : felt}(_class_hash : felt){
    class_hash.write(_class_hash);
    return();
}

@view
func is_challenge_done {syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() -> (res : felt){
    let (res) = challenge_is_done.read();
    return(res,);
}

@view
func get_class_hash {syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr : felt}() -> (res : felt){
    let (res) = class_hash.read();
    return(res,);
}

@external
func test_my_password{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(_password : felt) -> (res : felt){
    let (read) = class_hash.read();
    let (res) = ITest_Password_Contract.library_call_test_password(
        class_hash=read, password=_password
    );
    if(res == 1){
        challenge_is_done.write(1);
        return(res,);
    }
    return (res,);
}
