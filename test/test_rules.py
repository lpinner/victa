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


def test_rule_nonnumeric():
    """Test a non-numeric rule ID"""
    expr = 'not a'

    Data = namedtuple('Data', ['attribute'])
    testdata = Data(attribute='abc')
    rule = Rule('a', 'attribute', 'in', 'test rule')

    rules = RuleSet({1: rule})
    with pytest.raises(NameError):
        assert rules.test(expr, testdata)


def test_rule_invalid():
    """Test invalid ruleset syntax"""
    expr = '1 not 2'

    Data = namedtuple('Data', ['attribute'])
    testdata = Data(attribute='abc')
    rule1 = Rule('a', 'attribute', 'in', 'test rule1')
    rule2 = Rule('x', 'attribute', 'in', 'test rule2')

    rules = RuleSet({1: rule1, 2: rule2})
    with pytest.raises(RuleSyntaxError):
        assert rules.test(expr, testdata)


def test_rule_invalid_re():
    """Test invalid re syntax"""

    with pytest.raises(RuleSyntaxError):
        rule = Rule('[a', 'attribute', 're', 'test rule1')


def test_rule_valid_re():
    """Test valid re syntax"""

    Data = namedtuple('Data', ['attribute'])
    testdata = Data(attribute='abcd')

    rule1 = Rule('bc', 'attribute', 're', 'test rule1')
    rule2 = Rule('.*c.*', 'attribute', 're', 'test rule2')
    rule3 = Rule('(c)', 'attribute', 're', 'test rule3')
    ruleset = RuleSet({1: rule1, 2: rule2, 3: rule3})
    expr = '1 or 2 or 3'
    assert ruleset.test(expr, testdata)


def test_rule_floating_point():
    """Test floating point comparisons"""
    expr = '1'

    Data = namedtuple('Data', ['attribute'])
    testdata = Data(attribute=5.0)
    rule1 = Rule('5', 'attribute', 'equal', 'test rule1')

    rules = RuleSet({1: rule1})
    assert rules.test(expr, testdata)


def test_rule_gt_ge():
    """Test greater than comparisons"""
    expr = '1 and 2 and 3 and 4 and 5 and 6'

    Data = namedtuple('Data', ['attribute'])
    testdata = Data(attribute=5.0)

    rule1 = Rule('4', 'attribute', '>', 'test rule1')
    rule2 = Rule('4', 'attribute', 'gt', 'test rule3')
    rule3 = Rule('5', 'attribute', '>=', 'test rule3')
    rule4 = Rule('5', 'attribute', 'ge', 'test rule4')
    rule5 = Rule('4', 'attribute', '>=', 'test rule5')
    rule6 = Rule('4', 'attribute', 'ge', 'test rule6')

    rules = RuleSet({
        1: rule1,
        2: rule2,
        3: rule3,
        4: rule4,
        5: rule5,
        6: rule6,
    })
    assert rules.test(expr, testdata)


def test_rule_lt_le():
    """Test less than comparisons"""
    expr = '1 and 2 and 3 and 4 and 5 and 6'

    Data = namedtuple('Data', ['attribute'])
    testdata = Data(attribute=5.0)

    rule1 = Rule('6', 'attribute', '<', 'test rule1')
    rule2 = Rule('6', 'attribute', 'lt', 'test rule3')
    rule3 = Rule('5', 'attribute', '<=', 'test rule3')
    rule4 = Rule('5', 'attribute', 'le', 'test rule4')
    rule5 = Rule('6', 'attribute', '<=', 'test rule5')
    rule6 = Rule('6', 'attribute', 'le', 'test rule6')

    rules = RuleSet({
        1: rule1,
        2: rule2,
        3: rule3,
        4: rule4,
        5: rule5,
        6: rule6,
    })
    assert rules.test(expr, testdata)



