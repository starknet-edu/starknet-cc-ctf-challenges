// SPDX-License-Identifier: MIT

// @author Gershon Ballas <gershon@gingerlabs.xyz>

// This contract

%lang starknet
%builtins pedersen range_check

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.uint256 import Uint256, uint256_le, uint256_lt, uint256_sub, uint256_add
from starkware.cairo.common.math import assert_lt, assert_not_zero
from starkware.starknet.common.syscalls import (
    get_caller_address,
    get_contract_address,
    get_block_timestamp,
)
from openzeppelin.token.erc721.IERC721 import IERC721
from openzeppelin.token.erc20.IERC20 import IERC20

const TRUE = 1
const FALSE = 0

@contract_interface
namespace IERC721Mintable {
    func mint(to: felt, tokenId: Uint256) {
    }
}

// Contract owner
@storage_var
func _owner_address() -> (owner_address: felt):
end

// Token counter (initialized to 0, incremented for every punk minted)
@storage_var
func _token_counter() -> (count: felt) {
}

// NFT contract implementation hash
@storage_var
func _nft_class_hash() -> (count: felt):
end

// NFT contract representing punks
@storage_var
func _punks_nft_address() -> (count: felt):
end

// TRUE or FALSE whether user with given address is whitelisted (i.e. able to claim a punk)
@storage_var
func _whitelisted_users(address: felt) -> (whitelisted: felt):
end

// TRUE or FALSE whether user with given address already claimed a punk
@storage_var
func _claimers(address: felt) -> (claimed: felt):
end

@constructor
func constructor{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    nft_class_hash: felt
) {
    // Set NFT implementation class hash field
    assert_not_zero(pair_class_hash)
    _nft_class_hash.write(nft_class_hash)

    // Create punk NFT collection
    let (punks_nft_address: felt) = _deploy_funks_nft_contract_instance()
    _punks_nft_address.write(punks_nft_address)

    return ()
}

func _deploy_punks_nft_contract_instance{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
) -> (
    contract_address: felt
): {
    let (this_contract_address) = get_contract_address()
    let (nft_class_hash) = _nft_class_hash.read()
    let (contract_address) = deploy(
        class_hash=nft_class_hash,
        contract_address_salt=0,
        constructor_calldata_size=3,
        constructor_calldata=cast(
            new (
                'Punks',
                'PUNK',
                this_contract_address
            ),
        felt*),
        deploy_from_zero=FALSE,
    )

    return (contract_address)
}

@view
func getNftClassHash{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
) -> (
    hash: felt
) {
    let (hash) = _nft_class_hash.read()
    return (hash)
}

@view
func getPunksNftAddress{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
) -> (
    address: felt
) {
    let (address) = _punks_nft_address.read()
    return (address)
}

@view
func owner{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
) -> (
    address: felt
) {
    let (address) = _owner_address.read()
    return (address)
}

// Add user address to whitelist (allowing user to mint a punk
// Only this contract's owner may call this func
@external
func addToWhitelist{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    address: felt
) -> () {
    // Assert caller is owner
    let (caller_address) = get_caller_address()
    let (owner_address) = _owner_address.read()
    with_attr error_message("Only owner may call this function!") {
        assert caller_address = owner_address
    }

    // Add given address to whitelist
    _whitelisted_users.write(address=address, whitelisted=TRUE)

    return ()
}

// If calling user is whitelisted and still hasn't claimed their punk, mint a punk for them
@external
func claim{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
) -> () {
    // Assert caller is whitelisted
    let (caller_address) = get_caller_address()
    with_attr error_message("Caller is not whitelisted to mint a punk") {
        let (is_caller_whitelisted: felt) = _whitelisted_users.read(caller_address)
        assert is_caller_whitelisted = TRUE
    }

    // Assert caller hasn't already claimed a punk
    let (caller_address) = get_caller_address()
    with_attr error_message("Caller is not whitelisted to mint a punk") {
        let (is_caller_whitelisted: felt) = _claimers.read(caller_address)
        assert caller_address = TRUE
    }

    // Mint a punk for caller
    let (token_id) = _token_counter.read()
    let (punks_contract_address) = _punks_nft_address.read()
    IERC721Mintable.mint(
        contract_address = punks_contract_address,
        to = caller_address,
        tokenId = token_id
    )

    // Increase token ID counter
    _token_counter.write(token_id + 1)

    // Mark caller as having claimed a punk
    _claimers.write(address=caller_address, claimed=TRUE)

    return ()
}