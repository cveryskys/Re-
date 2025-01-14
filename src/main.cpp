#include <iostream>
#include "injector.h"

int main() {
    DWORD processID;
    std::string dllPath;

    std::cout << "Enter the process ID: ";
    std::cin >> processID;

    std::cout << "Enter the path to the DLL: ";
    std::cin >> dllPath;

    if (InjectDLL(processID, dllPath.c_str())) {
        std::cout << "DLL injected successfully!" << std::endl;
    } else {
        std::cout << "DLL injection failed!" << std::endl;
    }

    return 0;
}
