@echo off
setlocal 

pushd %~dp0

IF EXIST _build\NUL rmdir /q /s _build 
IF EXIST _source\NUL rmdir /q /s _source 
sphinx-apidoc -f -o apidoc ..\victa
call make html

rem TIMEOUT /T 1 /NOBREAK
rmdir /q /s doctrees
rmdir /q /s apidoc
ren html apidoc
move apidoc ../../apidoc

:EXIT