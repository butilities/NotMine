#!/usr/bin/python

# disable the unsigned driver warnings in Windows XP

import sys
import os
from _winreg import *
import win32security 


def complement(n,radix=32):
    if n < (1<<(radix-1)) : return n   
    else : return n - (1<<radix)       

def reg_write():

        sys.stdout.write("Connecting to registry     ")
        aReg = ConnectRegistry(None, HKEY_USERS)
        sys.stdout.write("[ OK ]")
        sys.stdout.write("\nWriting registry entry    ")
        username = 'Admin'
        sid = win32security.ConvertSidToStringSid(win32security.LookupAccountName(None, username)[0])
        keyVal = r'%s\Software\Policies\Microsoft\Windows NT\Driver Signing' % sid
        try:
                key = OpenKey(aReg, keyVal, 0, KEY_ALL_ACCESS)
        except:
                key = CreateKey(aReg, keyVal)

        SetValueEx(key, "BehaviorOnFailedVerify", 0, REG_DWORD, complement(0x00000000))
        sys.stdout.write("[ OK ]\n")
        sys.stdout.write("Cleaning up    ")
        CloseKey(key)
        CloseKey(aReg)
        sys.stdout.write("[ OK ]\n")
        sys.exit("We're done here.")

def main():
        reg_write()


if __name__ == '__main__':
        main()