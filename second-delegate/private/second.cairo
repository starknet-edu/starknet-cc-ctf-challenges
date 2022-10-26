%lang starknet

@contract_interface
namespace ITest_Password_Contract{
    func test_password(password : felt) -> (res : felt){
    }
}

const PASSWORD = 1575;

@view
func test_password{syscall_ptr : felt*, range_check_ptr}(password : felt) -> (res : felt){
    tempvar res :felt ;
    tempvar test = PASSWORD * 3; 
    tempvar test1 = test - 9;
    if (password == PASSWORD - 60) {
        res = 1;
    } else {
        res = 0;
    }
    return (res,);
}