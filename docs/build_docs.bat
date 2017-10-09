@echo off
setlocal 

pushd %~dp0
echo %CD%

IF EXIST _build\NUL rmdir /q /s _build _source 
sphinx-apidoc -f -o _source ..\victa
make html
rmdir /q /s _build _source 
