import os
import pandas.io.parsers

#Monkey patch for pygraphviz.agraph.AGraph._which
def _which(self, name):
    return which(name)

# Code from shutil.which - python 3.3+
# https://github.com/python/cpython/blob/master/Lib/shutil.py#L1096
# PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2
def shutil_which(cmd, mode=os.F_OK | os.X_OK, path=None):
    """Given a command, mode, and a PATH string, return the path which
    conforms to the given mode on the PATH, or None if there is no such
    file.
    `mode` defaults to os.F_OK | os.X_OK. `path` defaults to the result
    of os.environ.get("PATH"), or can be overridden with a custom search
    path.
    """

    # Check that a given file can be accessed with the correct mode.
    # Additionally check that `file` is not a directory, as on Windows
    # directories pass the os.access check.
    def _access_check(fn, mode):
        return (os.path.exists(fn) and os.access(fn, mode)
                and not os.path.isdir(fn))

    # If we're given a path with a directory part, look it up directly rather
    # than referring to PATH directories. This includes checking relative to the
    # current directory, e.g. ./script
    if os.path.dirname(cmd):
        if _access_check(cmd, mode):
            return cmd
        return None

    if path is None:
        path = os.environ.get("PATH", os.defpath)
    if not path:
        return None
    path = path.split(os.pathsep)

    if sys.platform == "win32":
        # The current directory takes precedence on Windows.
        if not os.curdir in path:
            path.insert(0, os.curdir)

        # PATHEXT is necessary to check on Windows.
        pathext = os.environ.get("PATHEXT", "").split(os.pathsep)
        # See if the given file matches any of the expected path extensions.
        # This will allow us to short circuit when given "python.exe".
        # If it does match, only test that one, otherwise we have to try
        # others.
        if any(cmd.lower().endswith(ext.lower()) for ext in pathext):
            files = [cmd]
        else:
            files = [cmd + ext for ext in pathext]
    else:
        # On other platforms you don't have things like PATHEXT to tell you
        # what file suffixes are executable, so just pass on cmd as-is.
        files = [cmd]

    seen = set()
    for dir in path:
        normdir = os.path.normcase(dir)
        if not normdir in seen:
            seen.add(normdir)
            for thefile in files:
                name = os.path.join(dir, thefile)
                if _access_check(name, mode):
                    return name
    return None

def _isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    #https://www.python.org/dev/peps/pep-0485
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

# Monkey patch for pygraphviz.agraph.AGraph._which
try:
    from shutil import which
except ImportError:
    which = shutil_which

# Backport py 3.5+ isclose
try:
    from cmath import isclose
except ImportError:
    isclose = _isclose

# Monkey patch for read_* to not interpret 'N/A' & 'NA' as NaN
# This is an ugly hack and really *should* be implemented by library users by passing by passing na_values=[], keep_default_na=False to their pandas.read_* calls
pandas.io.parsers._NA_VALUES = {'-1.#QNAN', '-nan', '', '-NaN', '#NA', 'N/A', 'NaN', '#N/A', '1.#QNAN', '1.#IND', 'nan', 'NULL', '-1.#IND', '#N/A N/A'}
