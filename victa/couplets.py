__all__ = ['Couplet']

from collections import namedtuple
import pandas as pd


class Couplet(namedtuple('Couplet', ['id', 'type', 'name', 'comments'])):
    """namedtuple: lightweight class for couplets"""
    __slots__ = ()
    def __new__(cls, id, type, name, comments=''):
        """Make comments optional"""
        return super(Couplet, cls).__new__(cls,  id, type, name, comments)

    def to_series(self):
        """Convert to a pandas.Series"""
        return pd.Series(self, self._fields)
