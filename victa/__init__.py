"""
VICTA

Author:
    Luke Pinner (ERIN)

TODO:
    - Package level doc

"""
__version__ = '2.4'

__all__ = ['build_rules',
           'build_key',
           'ClassificationError',
           'MultipleMatchesError',
           'Couplet',
           'Key',
           'Rule',
           'RuleSet',
           'RuleSyntaxError',
           ]

from .couplets import Couplet
from .errors import (RuleSyntaxError, ClassificationError, MultipleMatchesError)
from .key import (Key, build_key)
from .rules import (Rule, RuleSet, build_rules)
from .utils import *  # ensure patches are applied

