%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.starknet.common.syscalls import get_block_number
from starkware.cairo.common.math import unsigned_div_rem
from starkware.starknet.common.syscalls import get_caller_address

@storage_var
func counter(user : felt) -> (res : felt){
}

@storage_var
func password() -> (res : felt){
}

@storage_var
func challenge_is_done() -> (res: felt) {
}

@storage_var
func last_block() -> (res: felt) {
}



@constructor
func constructor{syscall_ptr : felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(_password : felt){
    password.write(_password);
    return ();
}

@external
func increase_counter{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr,
}(){
    alloc_locals;
    let (block_number) = get_block_number();
    let(q, r) = unsigned_div_rem(block_number, 5);
    let (last : felt) = last_block.read();
    if (r == 0 and block_number != block_number){
        let (user) = get_caller_address();
        let (res) = counter.read(user=user);
        counter.write(user, res + 1);
        last_block.write(block_number);
        return ();
    }
    return();
}

@external
func test_password{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr,
}(_password : felt) -> (res : felt){
    alloc_locals;
    let (user) = get_caller_address{}();
    let (counter_value) = counter.read(user=user);
    let (real_password : felt) = password.read();
    if (counter_value == 4 and real_password == _password){
        challenge_is_done.write(1);
        return(res=1);
    }
    return (res=0);
}