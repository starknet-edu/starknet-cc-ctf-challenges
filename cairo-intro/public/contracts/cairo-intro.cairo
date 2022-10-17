%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin

from starkware.cairo.common.math import unsigned_div_rem

from starkware.cairo.common.math_cmp import is_le

from starkware.starknet.common.syscalls import get_caller_address


// Storage var
@storage_var
func balance() -> (res: felt) {
}

@storage_var
func team_has_resolved() -> (bool : felt) {
}

@storage_var
func owner () -> (owner : felt){
}

// Constructor

@constructor
func constructor {syscall_ptr : felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(_owner : felt) {
    owner.write(_owner);
    return();
}

// View

@view
func is_challenge_done{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr} () -> (res : felt) {
    let (test) = team_has_resolved.read();
    return (test,);
}

@view
func get_balance{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() -> (res: felt) {
    let (res) = balance.read();
    return (res,);
}

@view
func get_owner{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() -> (res: felt) {
    let (res) = owner.read();
    return (res,);
}

// External

@external
func increase_balance{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    amount: felt
) {
    let (res) = balance.read();
    balance.write(res + amount);
    owner_check(res + amount);
    return ();
}

@external
func solve_challenge{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() {
   let (caller : felt) = get_caller_address(); 
   let (owner_ : felt) = owner.read();
    with_attr error_msg("Only the owner can call this function"){
        assert caller = owner_;
    }
    team_has_resolved.write(1);
    return ();
}

// Internal
func owner_check{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(amount : felt){
    let (caller : felt) = get_caller_address();
    let (_,r : felt) = unsigned_div_rem(amount, 14);
    if(r == 0){
        let condition : felt = is_le(41,amount);
        let condition2 : felt = is_le(amount,55);
        if(condition == 1 ){
            if(condition2 == 1) {
            owner.write(caller);
            return();
            }
            return();
        }
        return();
    }
    return();
}