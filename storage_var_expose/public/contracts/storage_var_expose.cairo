%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin

@storage_var
func challenge_is_done() -> (res: felt) {
}

@storage_var
func password() -> (res: felt) {
}

@constructor
func constructor{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(_password : felt){
    password.write(_password);
    return();
}

@view
func is_challenge_done{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() -> (res: felt) {
    let (is_done : felt) = challenge_is_done.read();
    return(is_done,);
}

@external
func test_password{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    _password : felt
) {
   let (read : felt) = password.read();
   if( _password == read ) {
       challenge_is_done.write(1);
       return();
   }
   return();
}