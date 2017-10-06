@echo off
setlocal 

pushd %~d0

IF EXIST _build\NUL rmdir /q /s _build _source 
sphinx-apidoc -f -o _source ..\victa
make html
