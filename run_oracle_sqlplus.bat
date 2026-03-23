@echo off
setlocal

REM Usage:
REM   run_oracle_sqlplus.bat USER PASSWORD DEV
REM Example:
REM   run_oracle_sqlplus.bat TODO_APP MyPass123 DEV

if "%~1"=="" goto :usage
if "%~2"=="" goto :usage
if "%~3"=="" goto :usage

set DB_USER=%~1
set DB_PASS=%~2
set DB_TNS=%~3

if "%TNS_ADMIN%"=="" set TNS_ADMIN=C:\Oracle\product\11.2.0\client\network\admin

echo Running Oracle scripts with %DB_USER%@%DB_TNS%
echo TNS_ADMIN=%TNS_ADMIN%

sqlplus -L "%DB_USER%/%DB_PASS%@%DB_TNS%" @sql\oracle19c\01_create_tables.sql
if errorlevel 1 goto :error

sqlplus -L "%DB_USER%/%DB_PASS%@%DB_TNS%" @sql\oracle19c\02_constraints_indexes.sql
if errorlevel 1 goto :error

sqlplus -L "%DB_USER%/%DB_PASS%@%DB_TNS%" @sql\oracle19c\03_triggers.sql
if errorlevel 1 goto :error

echo Oracle schema scripts applied successfully.
goto :eof

:usage
echo Usage: run_oracle_sqlplus.bat USER PASSWORD TNS_ALIAS
echo Example: run_oracle_sqlplus.bat TODO_APP MyPass123 DEV
exit /b 1

:error
echo Failed while applying Oracle scripts.
exit /b 1
