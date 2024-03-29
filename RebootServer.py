# RebootServer.py 
# Reboots using win32api

import win32security
import win32api
import sys
import time
from ntsecuritycon import *

def AdjustPrivilege(priv, enable = 1):
     # Get the process token.
     flags = TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY
     htoken = win32security.OpenProcessToken(win32api.GetCurrentProcess(), flags)
     # Get the ID for the system shutdown privilege.
     id = win32security.LookupPrivilegeValue(None, priv)
     # Now obtain the privilege for this process.
     # Create a list of the privileges to be added.
     if enable:
         newPrivileges = [(id, SE_PRIVILEGE_ENABLED)]
     else:
         newPrivileges = [(id, 0)]
     # and make the adjustment.
     win32security.AdjustTokenPrivileges(htoken, 0, newPrivileges)

def RebootServer(message="Post Install Reboot", timeout=5, bForce=0, bReboot=1):
     AdjustPrivilege(SE_SHUTDOWN_NAME)
     try:
         win32api.InitiateSystemShutdown(None, message, timeout, bForce, bReboot)
     finally:
         # Now we remove the privilege we just added.
         AdjustPrivilege(SE_SHUTDOWN_NAME, 0)

if __name__=='__main__':
    message = "Server rebooting in 10 seconds\r\n"
    RebootServer()
         