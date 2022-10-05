%lang starknet

@storage_var
func owner() -> (res: felt) {
}

const real_password = 592965625081988036501471237208223793;

@view
func test_password(password : felt) -> (res : felt){
    if (real_password == password){
        return (res= 1);
    }
    return (res= 0);
}