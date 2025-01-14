#include <iostream>
#include "injector.h"

int main() {
    std::cout << "Welcome to Redax Executor!" << std::endl;
    
    DWORD processID = 1234; 
    InjectDLL(processID, "dll/sample.dll");
    
    return 0;
}
