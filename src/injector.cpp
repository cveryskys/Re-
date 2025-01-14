#include <windows.h>
#include <iostream>

bool InjectDLL(DWORD processID, const char* dllPath) {
    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, processID);
    if (!hProcess) {
        std::cerr << "Failed to open process!" << std::endl;
        return false;
    }

    void* allocMem = VirtualAllocEx(hProcess, NULL, strlen(dllPath) + 1, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    if (!allocMem) {
        std::cerr << "Failed to allocate memory in target process!" << std::endl;
        CloseHandle(hProcess);
        return false;
    }

    WriteProcessMemory(hProcess, allocMem, dllPath, strlen(dllPath) + 1, NULL);

    HANDLE hThread = CreateRemoteThread(hProcess, NULL, 0, (LPTHREAD_START_ROUTINE)LoadLibraryA, allocMem, 0, NULL);
    if (!hThread) {
        std::cerr << "Failed to create remote thread!" << std::endl;
        CloseHandle(hProcess);
        return false;
    }

    CloseHandle(hThread);
    CloseHandle(hProcess);
    return true;
}
