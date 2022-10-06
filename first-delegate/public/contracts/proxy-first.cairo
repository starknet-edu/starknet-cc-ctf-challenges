%lang starknet

const real_password = 314159265359;

@view
func test_password(password : felt) -> (res : felt){
    if (real_password == password){
        return (res= 1);
    }
    return (res= 0);
}