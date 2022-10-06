%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin

@contract_interface
namespace ITestpasswordContract{
    func test_password(your_password : felt) -> (res : felt){
    }
}

@storage_var
func challenge_is_done() -> (bool: felt) {
}

@storage_var
func proxy() -> (challenge: felt) {
}

@constructor
func constructor{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(proxy_admin : felt) {
    proxy.write(proxy_admin);
    return();
}

@view
func is_challenge_done {syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}() -> (bool : felt){
    let (status ) = challenge_is_done.read();
    return(status,);
}

@external
func test_password{syscall_ptr : felt*,pedersen_ptr : HashBuiltin*, range_check_ptr}(your_password : felt) -> (){
    let (proxy_admin : felt) = proxy.read();
    let (res) = ITestpasswordContract.test_password(
        contract_address=proxy_admin, your_password=your_password
    );
    if(res == 1){
        challenge_is_done.write(1);
        return();
    }
    return ();
}