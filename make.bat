@ECHO OFF

pushd %~dp0

if "%BUILDDIR%" == "" (
	set BUILDDIR=..\build
)
if "%DISTDIR%" == "" (
	set DISTDIR=..\dist
)

python setup.py sdist --dist-dir="%DISTDIR%"
python setup.py bdist_wheel --dist-dir="%DISTDIR%" --bdist-dir="%BUILDDIR%"  --universal
rmdir /q /s build 
rmdir /q /s VICTA.egg-info 

:end
popd
