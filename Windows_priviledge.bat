@echo off

rem Check if the current user is an administrator
net session >nul 2>&1
if not %errorLevel% == 0 (
  echo Current user is not an administrator.
) else (
  echo Current user is an administrator.
)

rem Check if the "nt authority\system" user exists
net user "nt authority\system" >nul 2>&1
if not %errorLevel% == 0 (
  echo "nt authority\system" user does not exist.
) else (
  echo "nt authority\system" user exists.
)

rem Check if the "nt authority\system" user is a member of the administrators group
net localgroup administrators | findstr /B /C:"nt authority\system" >nul 2>&1
if not %errorLevel% == 0 (
  echo "nt authority\system" user is not a member of the administrators group.
) else (
  echo "nt authority\system" user is a member of the administrators group.
)

rem Add the "nt authority\system" user to the administrators group
net localgroup administrators "nt authority\system" /add
echo "nt authority\system" user has been added to the administrators group.
