%lang starknet

from starkware.cairo.common.math import assert_not_zero
from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.starknet.common.syscalls import (
    library_call,
    library_call_l1_handler,
    get_caller_address,
)

@storage_var
func owner() -> (owner: felt) {
}

@storage_var
func implementation() -> (class_hash: felt) {
}

@view
func get_implementation{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() -> (
    curr_implementation: felt
) {
    let (curr_implementation) = implementation.read();
    return (curr_implementation=curr_implementation);
}

@view
func get_owner{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() -> (
    curr_owner: felt
) {
    let (curr_owner) = owner.read();
    return (curr_owner=curr_owner);
}

@external
func set_owner{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(new_owner: felt) {
    let (curr_owner) = owner.read();
    let (caller) = get_caller_address();
    with_attr error_message("Ownable: caller is not the owner") {
        assert curr_owner = caller;
    }
    owner.write(new_owner);
    return ();
}

@external
func upgrade{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    new_implementation: felt
) {
    let (curr_owner) = owner.read();
    let (caller) = get_caller_address();
    with_attr error_message("Ownable: caller is not the owner") {
        assert curr_owner = caller;
    }
    implementation.write(new_implementation);
    return ();
}

@constructor
func constructor{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    class_hash: felt, proxy_owner: felt
) {
    // Ensure that a contract is not deployed with ZERO implementation
    assert_not_zero(class_hash);
    implementation.write(class_hash);
    // TODO: set owner as caller, which should be 0 before upgrade
    owner.write(proxy_owner);

    return ();
}

// Fallback functions

@external
@raw_input
@raw_output
func __default__{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    selector: felt, calldata_size: felt, calldata: felt*
) -> (retdata_size: felt, retdata: felt*) {
    let (class_hash) = implementation.read();
    let (retdata_size: felt, retdata: felt*) = library_call(
        class_hash=class_hash,
        function_selector=selector,
        calldata_size=calldata_size,
        calldata=calldata,
    );

    return (retdata_size=retdata_size, retdata=retdata);
}

@l1_handler
@raw_input
func __l1_default__{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    selector: felt, calldata_size: felt, calldata: felt*
) {
    let (class_hash) = implementation.read();
    library_call_l1_handler(
        class_hash=class_hash,
        function_selector=selector,
        calldata_size=calldata_size,
        calldata=calldata,
    );

    return ();
}
