#!/usr/bin/python

import sys
import os
from ctypes import *
from win32api import GetFileVersionInfo, LOWORD, HIWORD

class OSVERSIONINFO(Structure):
    _fields_ = [ 
        ('dwOSVersionInfoSize', c_ulong),
        ('dwMajorVersion', c_ulong),
        ('dwMinorVersion', c_ulong),
        ('dwBuildNumber', c_ulong),
        ('dwPlatformId', c_ulong),
        ('szCSDVersion[128]', c_byte * 128)
    ]
    
class SYSTEM_INFO(Structure):
    _fields_ = [
        ('wProcessorArchitecture', c_ushort),
        ('wReserved', c_ushort),
        ('dwPageSize;', c_ulong), 
        ('lpMinimumApplicationAddress', c_void_p),
        ('lpMaximumApplicationAddress',  c_void_p),
        ('dwActiveProcessorMask', c_ulong),
        ('dwNumberOfProcessors', c_ulong), 
        ('dwProcessorType', c_ulong),
        ('dwAllocationGranularity', c_ulong),
        ('wProcessorLevel', c_ushort),
        ('wProcessorRevision', c_ushort)
    ]   

osinfo = OSVERSIONINFO()
osinfo.dwOSVersionInfoSize = sizeof(osinfo)
if windll.kernel32.GetVersionExA(byref(osinfo)) == 0:
    print "[FAIL] Unable to determine Operating System version (%d)" % windll.kernel32.GetLastError()
    sys.exit(0)

if osinfo.dwMajorVersion == 5 and osinfo.dwMinorVersion == 1:
    opsys = "Windows XP"
elif osinfo.dwMajorVersion == 6 and osinfo.dwMinorVersion == 1:
    opsys = "Windows 7"


print opsys