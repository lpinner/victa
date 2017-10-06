"""
TODO Docstring
"""
__all__ = ['Rule', 'RuleSet', 'RuleSyntaxError']

import ast
import pandas as pd


class RuleSyntaxError(SyntaxError):
    """ Custom Exception raised when rule parsing fails"""
    pass


class Rule(object):
    """
    Build a callable Rule object.

    The instantiated Rule will return True or False when called with a record to test against.

    Args:
        value (str): text string to look for
        attribute (str): attribute/column to use when rule is tested
        operator (str): positive comparison operator (currently only `in` and `equal`)
        name (str): Rule name
        comment (str, optional): Additional comments

    Returns:
        rule: victa.Rule

    """
    def __init__(self, value, attribute, operator, name, comment=''):
        """

        Returns:
            object:
        """
        self.value = str(value).strip().upper() ## TODO think about/handle case. What about regexes?
        self.attribute = str(attribute).strip()
        self.operator = str(operator).strip()
        self.name = str(name).strip()
        self.comment = str(comment).strip()

    def _equal(self, value):
        return value == self.value

    def _in(self, value):
        return self.value in value

    def __call__(self, record):
        """
        Test a rule against a record
        Args:
            record:

        Returns:
            Bool:
        """

        value = str(getattr(record, self.attribute)).upper()
        return getattr(self, '_' + self.operator)(value)


class RuleSet(dict):

    def test(self, expr, record):
        """
        Test a ruleset expression against a record
        Args:
            expr:
            record:

        Returns:
            Bool:

        """
        return eval(self._parse(expr), {}, {'self': self, 'record': record})

    def _parse(self, expr):
        """
        Magic happens here :)

        What this does is turn a string expression like `not (123 or 456)` into a compiled code object ready for
        evaluation, such as `not (ruleset[123](record) or ruleset[456](record))`

        We do this by assuming each integer is a rule ID and altering the expression using an ast.NodeTransformer to
        convert each integer node to a callable function

        Args:
            expr:

        Returns:
            code object:
        """
        transformer = RuleSetTransformer()
        expr = str(expr).strip() #str(expr) to handle pandas parsing '321' as int
                                 #.strip() to handle '" blah" is not valid python syntax, unexpected indent'
        try:
            ast_expr = ast.parse(expr, mode='eval')
            ast_expr = transformer.visit(ast_expr) #this automagically invokes RuleSetTransformer.visit_Num
            ast.fix_missing_locations(ast_expr)
            return compile(ast_expr, '', 'eval')
        except SyntaxError as err:
            raise RuleSyntaxError('The ruleset expression "{}" is not valid python syntax, {}'.format(expr, err.msg))


class RuleSetTransformer(ast.NodeTransformer):

    def visit_Num(self, node):
        """
        This function gets called by the transformer for each distinct numeric node (i.e 123).
        It will not get called for a alphanumeric node (i.e. abc123)

        Args:
            node (ast.node):

        Returns:
            node (ast.node):
        """
        ## TODO this is hard to debug, is there a better way?
        value = ast.Name(id='self', ctx=ast.Load())
        slice = ast.Index(value=node)
        func = ast.Subscript(value=value,slice=slice,ctx=ast.Load())

        call = ast.Call(func=func,
                        args=[ast.Name(id='record', ctx=ast.Load())],
                        keywords=[])
        return call


def build_rules(rules_df):
    """
    Build a RuleSet of Rule objects from a Pandas DataFrame containing the rule definitions

    Args:
        rules_df (pandas.DataFrame): dataframe containing the rules
            The dataframe must have the following column structure:
             - ID = unique integer identifying the rule
             - ATTRIBUTE = attribute/column to use when rule is tested (i.e. in the record to be classified by the key)
             - OPERATOR = positive comparison operator (currently only `in` and `equal`)
             - VALUE = text string to look for in ATTRIBUTE
             - NAME = Rule name
             - COMMENTS [optional] = Additional comments

    Returns:
        ruleset: victa.RuleSet
    """
    ruleset = RuleSet()
    for idx, row in rules_df.iterrows():
        rule_id = int(row['ID'])
        comment = '' if pd.isnull(row['COMMENTS']) else row['COMMENTS']

        rule = Rule(value=row['VALUE'],
                    attribute=row['ATTRIBUTE'],
                    operator=row['OPERATOR'],
                    name=row['NAME'],
                    comment=comment)
        ruleset[rule_id] = rule

    return ruleset
