%lang starknet

@contract_interface
namespace ITest_Password_Contract{
    func test_password(password : felt) -> (res : felt){
    }
}

@view
func test_my_password{syscall_ptr : felt*, range_check_ptr}(password : felt) -> (res : felt){

    let (res) = ITest_Password_Contract.library_call_test_password(
        class_hash=0xca379ac7953874cdcaa02331e627ace0508efb67d5bf7ed921eab154149ab4, password=password
    );
    return (res=res);
}
