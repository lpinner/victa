@ECHO OFF

pushd %~dp0

set SOURCEDIR=.
set BUILDDIR=../../apidoc
set SPHINXPROJ=VICTA
set PROJDIR=..\victa

sphinx-apidoc -f -o %BUILDDIR% %PROJDIR%
sphinx-build -M html %SOURCEDIR% %BUILDDIR%

:end
popd
