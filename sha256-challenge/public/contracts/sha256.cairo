%lang starknet

from starkware.cairo.common.alloc import alloc
from starkware.cairo.common.cairo_builtins import BitwiseBuiltin

from starkware.cairo.common.registers import get_fp_and_pc
from starkware.cairo.common.math import assert_nn_le, unsigned_div_rem
from starkware.cairo.common.memset import memset
from starkware.cairo.common.pow import pow

from starkware.cairo.common.cairo_builtins import HashBuiltin
from lib import sha256, finalize_sha256


@storage_var
func challenge_is_done() -> (res: felt) {
}

@view
func is_challenge_done{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() -> (
    res: felt
) {
    let (res) = challenge_is_done.read();
    return (res,);
}

func compute_sha256{range_check_ptr, bitwise_ptr: BitwiseBuiltin*}(
    input_len: felt, input: felt*, n_bytes: felt
) -> (res0: felt, res1: felt) {
    alloc_locals;

    let (local sha256_ptr_start: felt*) = alloc();
    let sha256_ptr = sha256_ptr_start;

    let (local output: felt*) = sha256{sha256_ptr=sha256_ptr}(input, n_bytes);
    finalize_sha256(sha256_ptr_start=sha256_ptr_start, sha256_ptr_end=sha256_ptr);

    return (
        output[3] + 2 ** 32 * output[2] + 2 ** 64 * output[1] + 2 ** 96 * output[0],
        output[7] + 2 ** 32 * output[6] + 2 ** 64 * output[5] + 2 ** 96 * output[4],
    );
}

@external
func test_password{
    syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr, bitwise_ptr: BitwiseBuiltin*
}(input_len: felt, input: felt*, n_bytes: felt) -> (res: felt) {
    alloc_locals;

    let (a, b) = compute_sha256(input_len, input, n_bytes);

    if (a == 0x1cf18a243c25a56a993c8207d1161a9c and b == 0x2de5f34b952d382704b94dc5e888b108) {
        challenge_is_done.write(1);
        return (res=1);
    }
    return (res=0);
}