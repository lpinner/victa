@ECHO OFF

if "%1" == "" goto dist
if "%1" == "dist" goto dist
if "%1" == "test" goto test
if "%1" == "doc" goto doc

:dist

    if "%BUILDDIR%" == "" (
        set BUILDDIR=build
    )
    if "%DISTDIR%" == "" (
        set DISTDIR=dist
    )
    REM python setup.py sdist --dist-dir="%DISTDIR%"
    python setup.py bdist_wheel --dist-dir="%DISTDIR%" --bdist-dir="%BUILDDIR%"  --universal
    rmdir /q /s build 
    rmdir /q /s VICTA.egg-info 
    goto end 

:test
    pytest
    goto end 

:doc
    pushd %~dp0docs
    set OUTPUTDIR=
    set SPHINXPROJ=VICTA
    set PROJDIR=victa

    sphinx-apidoc  -f -o "."  "../victa"
    sphinx-build -M html . .
    pandoc -o %~dp0README.docx -f markdown -t docx %~dp0README.md --reference-docx=reference.docx
    goto end 

:end
popd
