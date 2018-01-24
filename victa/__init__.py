"""
VICTA

Author:
    Luke Pinner (ERIN)

TODO:
    - Package level doc

"""

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

from .key import Key, ClassificationError, build_key
from .rules import Rule, RuleSet, build_rules
from .couplets import Couplet
from .errors import RuleSyntaxError, ClassificationError, MultipleMatchesError
from .utils import * # ensure patches are applied