#!/usr/bin/python

import sys
import os
from _winreg import *

def reg_write():
	
	sys.stdout.write("Connecting to registry     ")
	aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
	sys.stdout.write("[ OK ]")
	sys.stdout.write("\nWriting registry entry    ")
	keyVal = r'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
	try:
		key = OpenKey(aReg, keyVal, 0, KEY_ALL_ACCESS)
	except:
		key = CreateKey(aReg, keyVal)

	SetValueEx(key, "TestFile", 0, REG_SZ, '"C:\\Program Files\\Pwned\\yourmom.exe"')
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