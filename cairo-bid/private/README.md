## General idea and motivation
This challenge utilizes two confusing mechanisms in Cairo language:
- signed/unsigned numbers
- difference between representing negative `felt` and negative `Uint256`
### Signed/Uinsigned numbers
In Cairo signed and unsigned numbers are represented exactly the same way.
Whether the number is sigend or unsigned depends on interpretation, so practically depends on which comparison/math functions we use on those numbers.
### Negative signed numbers
Another thing is how signed negative numbers are represented with `felt` and with `Uint256`. Negative numbers are in fact "positive" numbers that in some are interpreted as negative numbers. This range differs between `felt` and `Uint256`:
Signed `felt` is positive in range `[0, 2**128)` and negative in range `[2**128, P)`.
Signed `Uint256` is dependent on `Uint256.high` member. So positive if `Uint256.high` is in range `[0, 2**127)` and negative if `Uint256.high` is in range `[2**127, 2**128)`.

### Motivation
I hope this challenge may turn developers' eyes on the issue with signed/unsigned and negative numbers in Cairo. Also hope people get some fun.

## Contract
Simple bidding contract where each user need to first transfer some funds and then bid. Each action can only be done once per address.

## Secnario

### Initial conditions
1. Challenge is initialized with initial balance of:
    owner: Uint256(1000, 0), attacker: Uint256(10, 0)
2. Onwer bidds with amount Uint256(1000, 0);

### Goal
Attacker needs to become the highest bidder and win the auction. It is seemingly impossible, since got balance of `10`, minimal bid is `100` and the current winner bids `1000`.

### Exploit
Attacker can win if adds bid amount equal negative value, e.g. `-1`. Since function takes `Uint256` type, it needs to be represented like this (assuming attacker bids `-1`) `uint256_neg(Uint256(1, 0))` i.e. the number is: `Uint256(2**128-1, 2**128-1)`.
The function `add_bid(...)` looks secure, since it does bunch of checks: `uint256_check(...)`, `check_minimal_bid(...)` and `check_if_enough_funds(...)`. But all those checks are passed with `-1`.
- The checks `uint256_check(...)` will pass, since the passed number is correct `Uint256` type.
- Another check is comparison of bid amount with balance of an attacker. Those amounts are represented as `Uint256` with function `uint256_signed_le(...)` (balance of attacker is transformed from `felt` to `Uint256`), so clearly `10` is higher than `-1`. Check passed.
- Last check is comparison of bid amount with minimal bid. Minimal bid is stored as a constant, so it makes sense to convert bid amount to `Uint256`. And here something interesting happens. Function `uint256_to_felt(...)` looks like it does secure conversion, because it would throw if `Uint256` value is too big to fit in `felt`. However this is not true, since if value in `Uint256` could just overflow, and the assertion is done on oveflown `felt` which is valid. After conversion from number `-1` represented as `Uint256` we get huge number represented in `felt` (precisely `3618502788666127798953978732740734578953660990361066340291730267701097005024`, but still less than `2**251` so `assert_251_bits` passes). And so the number transformed to `felt` is a huge number, that easily exceeds the minimal bid. The function used to compare `felt` amounts is: `is_le_felt(...)` and treats compared numbers as unsigned `felts`.
- Transformed `-1` into `felt` is also much greater than the current highest bid, so the attacker wins the auction.
