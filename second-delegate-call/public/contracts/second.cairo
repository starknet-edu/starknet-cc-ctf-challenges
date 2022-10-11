%lang starknet

@contract_interface
namespace ITest_Password_Contract{
    func test_password(password : felt) -> (res : felt){
    }
}

const PASSWORD = 1515;

@view
func test_password{syscall_ptr : felt*, range_check_ptr}(password : felt) -> (res : felt){
    tempvar res :felt ;
    if (password == PASSWORD) {
        res = 1;
    } else {
        res = 0;
    }
    return (res,);
}