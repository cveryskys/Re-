#pragma once

#include <windows.h>

bool InjectDLL(DWORD processID, const char* dllPath);
