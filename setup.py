from setuptools import setup
import victa

setup(
    name='VICTA',
    version=victa.__version__,
    packages=['victa'],
    url='https://github.com/lpinner/victa',
    license='Apache 2.0',
    author='Luke Pinner',
    author_email=' lpinner@users.noreply.github.com',
    description='Vegetation Information Classification Tool Automator (VICTA)',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: Apache Software License",
    ],
    install_requires=[
       'networkx',
       'pandas',
       'xlrd',
       'openpyxl'
    ]

)
