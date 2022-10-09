%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.uint256 import Uint256, uint256_check, uint256_signed_le
from starkware.cairo.common.bool import TRUE, FALSE
from starkware.cairo.common.math import is_le_felt
from utils import uint256_to_felt, felt_to_uint256

using Bool = felt;
using Address = felt;

// storing balance as felts for storage cost saving
@storage_var
func Bid_balance_of(address: Address) -> (balance: felt) {
}
// storing fact of address transfering funds
@storage_var
func Bid_transfer_fact(address: Address) -> (transfered: Bool) {
}
// storing fact of address bidding
@storage_var
func Bid_fact_bid(address: Address) -> (bidded: Bool) {
}
// storing bidded amount
@storage_var
func Bid_bid_amount(address: Address) -> (bid_amount: felt) {
}
// storing highest bidded amount and address of the bidder
@storage_var
func Bid_highest_bid() -> (bid_amount: felt, address: Address) {
}
// minimal bid amount
const minimal_bid = 100

namespace Bid{
    // transfering funds that can be used to bid
    func transfer_funds{pedersen_ptr: HashBuiltin*, range_check_ptr}(
            address: Address, amount: Uint256
    ) -> (success: Bool) {
        uint256_check(amount);

        let transfer_fact = Bid_transfer_fact.read(address);
        with_attr error_message("Given address already transfered funds!"){
            assert transfer_fact = FALSE;
        }
        Bid_transfer_fact.write(address, TRUE);

        let amount_felt = uint256_to_felt(amount);
        Bid_balance_of.write(address, amount_felt);

        return (TRUE,);
    }
    // add bid
    func add_bid{pedersen_ptr: HashBuiltin*, range_check_ptr}(
            address: Address, bid_amount: Uint256
    ) -> (success: Bool) {
        uint256_check(bid_amount);

        let bid_fact = Bid_fact_bid.read(address);
        with_attr error_message("Given address already bidded!"){
            assert bid_fact = FALSE;
        }

        check_if_enough_funds(address, bid_amount);
        check_minimal_bid(bid_amount);
        
        Bid_fact_bid.write(address, TRUE);

        let bid_amoun_felt = uint256_to_felt(bid_amount);
        Bid_bid_amount.write(address, bid_amoun_felt);

        let (current_winner_bid, _) = Bid_highest_bid.read();
        let is_bid_winner = is_lt_felt(current_winner_bid, bid_amoun_felt);
        if (is_bid_winner == TRUE) {
            Bid_highest_bid.write(bid_amoun_felt, address);
        }
        return (TRUE,);
    }
    // returns winner of an auction
    func get_winner{pedersen_ptr: HashBuiltin*, range_check_ptr}(
    ) -> (address: Address, bid_amount: felt) {
        let (winner_address, winner_bid_amount) = Bid_highest_bid.read();
        return (address, bid_amoun);
    }
    // check if user has enough amount to bid
    func check_if_enough_funds{pedersen_ptr: HashBuiltin*, range_check_ptr}(
        address: Address, bid_amount: Uint256
    ) {
        uint256_check(bid_amount);

        let user_balance = Bid_balance_of.read(address);
        let user_balance_uint256 = felt_to_uint256(user_amount);
        let user_got_enough_funds = uint256_signed_le(bid_amount, user_amount_uint256);
        with_attr error_message("Bid amount exceeds current balance!"){
            assert user_got_enough_funds = TRUE;
        }
        return ();
    }
    // check if bid is higher than minimal amount
    func check_minimal_bid{range_check_ptr}(
        bid_amount: Uint256
    ) {
        uint256_check(bid_amount);

        let amount_in_felt = uint256_to_felt(amount);
        let is_minimal_bid = is_le_felt(minimal_bid, amount_in_felt);
        with_attr error_message("Bid amount is less than minimal required!") {
            assert is_minimal_bid = TRUE;
        }
        return ();
    }

}

func is_lt_felt(
    a: felt, b: felt
) -> (res: Bool) {
    if (a == b) {
        return FALSE;
    }
    let (is_a_le_b) = is_le_felt(a, b);
    return is_a_le_b;
}
