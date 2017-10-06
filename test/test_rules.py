import pytest
from collections import namedtuple
from victa.rules import Rule, RuleSet, RuleSyntaxError


def test_ruleset1():
    '''test ruleset with `not` expr return False'''
    expr = 'not 123'

    rule = lambda x: True
    ruleset = RuleSet({123: rule})
    assert not ruleset.test(expr, 'None')


def test_ruleset2():
    '''test ruleset with `or` expr returns True'''
    expr = '(123 or 456)'

    rule = lambda x: True
    ruleset = RuleSet({123: rule, 456: rule})
    assert ruleset.test(expr, 'None')


def test_ruleset3():
    '''test ruleset with `not` and `and` expr returns True'''
    expr = 'not (123 and 456)'

    rule123 = lambda x: True
    rule456 = lambda x: False
    ruleset = RuleSet({123: rule123, 456: rule456})
    assert ruleset.test(expr, 'None')

def test_ruleset4():
    '''test ruleset with `not` and `or` expr return False'''
    rule = lambda x: True

    ruleset = RuleSet({123: rule, 456: rule})
    expr = 'not (123 or 456)'
    assert not ruleset.test(expr, 'None')


def test_rule1():
    """Test a non-numeric rule ID"""
    expr = 'not a'

    Data = namedtuple('Data', ['attribute'])
    testdata = Data(attribute='abc')
    rule = Rule('a', 'attribute', 'in', 'test rule')

    rules = RuleSet({1: rule})
    with pytest.raises(NameError):
        assert rules.test(expr, testdata)


def test_rule2():
    """Test invalid ruleset syntax"""
    expr = '1 not 2'

    Data = namedtuple('Data', ['attribute'])
    testdata = Data(attribute='abc')
    rule1 = Rule('a', 'attribute', 'in', 'test rule1')
    rule2 = Rule('x', 'attribute', 'in', 'test rule2')

    rules = RuleSet({1: rule1, 2: rule2})
    with pytest.raises(RuleSyntaxError):
        assert rules.test(expr, testdata)



