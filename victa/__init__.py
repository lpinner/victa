"""
VICTA

Author:
    Luke Pinner (ERIN)

TODO:
    - Package level doc

"""

__all__ = ['Key', 'ClassificationError', 'Rule', 'RuleSet', 'RuleSyntaxError', 'Couplet', 'build_rules', 'build_key']

from .key import Key, ClassificationError, build_key
from .rules import Rule, RuleSet, build_rules
from .couplets import Couplet
from .errors import RuleSyntaxError, ClassificationError, MultipleMatchesError