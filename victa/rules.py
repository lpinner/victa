"""
TODO Docstring
"""
__all__ = ['Rule', 'RuleSet']

import ast
import pandas as pd
import re
import sre_constants

from .errors import RuleSyntaxError, ManadatoryFieldError
from .utils import isclose

class Rule(object):
    """
    Build a callable Rule object.

    The instantiated Rule will return True or False when called with a record to test against.

    Args:
        value (str): text string to look for
        attribute (str): attribute/column to use when rule is tested
        operator (str): positive comparison operator: :code:`in`, :code:`=`, :code:`>=`, :code:`>`, :code:`<=`, :code:`<`, :code:`regex`
            where: regex is a valid regular expression string (https://docs.python.org/3/library/re.html)
        name (str): Rule name
        comment (str, optional): Additional comments

    Returns:
        victa.Rule:

    """
    def __init__(self, value, attribute, operator, name, comment=''):
        """

        Returns:
            object:
        """
        self.operators = {   # Operator synonyms
            '=': self._equal,
            '==': self._equal,
            'equals': self._equal,
            'equal': self._equal, # Required for backwards compatibility
            'in': self._in,
            '>=': self._ge,
            'ge': self._ge,
            '>': self._gt,
            'gt': self._gt,
            '<=': self._le,
            'le': self._le,
            '<': self._lt,
            'lt': self._lt,
            're': self._re,
            'regex': self._re,
        }

        self.attribute = str(attribute).strip()
        self.operator = self.operators[str(operator).strip().lower()]

        if self.operator == self._re:
            try:
                self.value = re.compile(str(value).strip(), re.IGNORECASE)
            except sre_constants.error as e:
                raise RuleSyntaxError('Invalid regex syntax "{}": {}'.format(e.pattern, ','.join(e.args)))
        else:
            self.value = str(value).strip().upper() ## TODO think about/handle case. What about regexes?

        self.name = str(name).strip()
        self.comment = str(comment).strip()

    def _equal(self, value):
        try:
            return isclose(float(value), float(self.value))
        except ValueError:
            return value == self.value

    def _in(self, value):
        return self.value in value

    def _re(self, value):
        return True if self.value.search(value) else False

    def _ge(self, value):
        try:
            return float(value) >= float(self.value)
        except ValueError:
            return value >= self.value

    def _gt(self, value):
        try:
            return float(value) > float(self.value)
        except ValueError:
            return value > self.value

    def _le(self, value):
        try:
            return float(value) <= float(self.value)
        except ValueError:
            return value <= self.value

    def _lt(self, value):
        try:
            return float(value) < float(self.value)
        except ValueError:
            return value < self.value

    def __call__(self, record):
        """
        Test a rule against a record
        Args:
            record:

        Returns:
            Bool:
        """

        value = str(getattr(record, self.attribute)).strip().upper()
        return self.operator(value)


class RuleSet(dict):

    def test(self, expr, record):
        """
        Test a ruleset expression against a record

        Args:
            expr (str): string expression to be evaluated
            record (pandas.Series): record to test against expression

        Returns:
            Bool:

        """
        return eval(self._parse(expr), {}, {'self': self, 'record': record})

    def _parse(self, expr):
        """
        Magic happens here :)

        What this does is turn a string expression like :code:`not (123 or 456)` into a compiled code object ready for
        evaluation, such as :code:`not (ruleset[123](record) or ruleset[456](record))`

        We do this by assuming each integer is a rule ID and altering the expression using an ast.NodeTransformer to
        convert each integer node to a callable function

        Args:
            expr (str): string expression to be evaluated

        Returns:
            code (object):
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
             - OPERATOR =  positive comparison operator:
                :code:`in`, :code:`=`, :code:`>=`, :code:`>`, :code:`<=`, :code:`<`, :code:`regex`
                where: regex is a valid [regular expression](https://docs.python.org/3/library/re.html)
             - VALUE = text string to look for in ATTRIBUTE.
             - NAME = Rule name
             - COMMENTS [optional] = Additional comments

    Returns:
        ruleset: victa.RuleSet

    Note:
        -  Order for ordinal comparisons is ATTRIBUTE operator VALUE, i.e ATTRIBUTE >= 5.0
    """
    ruleset = RuleSet()
    for idx, row in rules_df.iterrows():
        # Ensure mandatory fields are not empty
        mandatory = ['ID', 'ATTRIBUTE', 'OPERATOR', 'VALUE', 'NAME']
        test = row.loc[mandatory]
        if test.isnull().any():
            fields = ', '.join(['"{}"'.format(m) for m in mandatory])
            values =  test.to_dict()
            raise ManadatoryFieldError('All of {} must contain a value: {}'.format(fields, values))

        rule_id = int(row['ID'])
        comment = '' if pd.isnull(row['COMMENTS']) else row['COMMENTS']

        rule = Rule(value=row['VALUE'],
                    attribute=row['ATTRIBUTE'],
                    operator=row['OPERATOR'],
                    name=row['NAME'],
                    comment=comment)
        ruleset[rule_id] = rule

    return ruleset
