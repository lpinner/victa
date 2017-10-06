# -*- coding: utf-8 -*-
"""

Classification Key

TODO:
    - Module level doc
"""

__all__ = ['Key', 'ClassificationError']

import pandas as pd
import networkx as nx

## TODO - decide plotting software and implement it properly, graphviz is a pain to install and uggghhhly
# import matplotlib.pyplot as plt
# import pygraphviz.agraph
# try:
#     from networkx.drawing.nx_agraph import graphviz_layout
# except ImportError:
#     from networkx import graphviz_layout
#
## Monkey patch for pygraphviz.agraph.AGraph._which
# from victa.utils import _which
# pygraphviz.agraph.AGraph._which = _which

from .rules import build_rules
from .couplets import Couplet


class ClassificationError(Exception):
    """ Custom Exception raised when classification fails"""
    pass


class Key(object):
    """ Classification Key

    """

    def __init__(self, key_df, key_desc, rules_df):
        """
         Build a Classification Key

         Args:
             key_df (pandas.DataFrame): see victa.key.build_key
             key_desc (str): see victa.key.build_key
             rules_df (pandas.DataFrame): see victa.key.build_rules
         """
        self.ruleset = build_rules(rules_df)
        self.key = build_key(key_df, key_desc)

    def classify(self, record):
        """
        Classify a record

        Args:
            record (pandas.Series): record to be classified
                record needs to contain all columns (Series axis labels) referred to in the `Rule`s
                see victa.rules.build_rules

        Returns:
            tuple(pandas.Series, pandas.Dataframe): the output class and a the couplets that were "followed"

        Raises:
            ClassificationError: When unable to classify a record

        TODO:
            - figure out a better way to stop infinite recursion
            - decide return data model
            - need a better word than "followed" in the docstring
        """
        # TODO need a better word than "followed" in the docstring

        visited = [self.key.root]

        ## TODO figure out a better way to stop infinite recursion
        #while True:
        for i in range(len(self.key.node)*2):

            for in_couplet, out_couplet, rules in self.key.edges_iter(visited[-1].id, data=True):

                couplet = self.key.node[out_couplet]['couplet']
                if self.ruleset.test(rules['ruleset'], record):
                    visited += [couplet]
                    if couplet.type == 'class':
                        # TODO decide return data model: tuple(pandas.Series, pandas.Dataframe), tuple(Couplet, list), etc...?
                        #return couplet, visited
                        visited = pd.DataFrame(visited)
                        return couplet.to_series(), visited.assign(step=visited.index)
                    break

        raise ClassificationError('Unable to classify record', record)

    def classify_iter(self, records):
        """
        Args:
            records (pandas.DataFrame): records to be classified
                records need to contain all columns (DataFrame axis labels) referred to in the `Rule`s
                see victa.key.build_rules

        Yields:
            tuple(pandas.Series, pandas.Dataframe, pandas.Series): the output class, a list of couplets
                that were "followed" and the input record
        Notes:
            Will yield tuple(None, None, pandas.Series) on ClassificationError
        """
        # TODO need a better word than "followed" in the docstring

        for idx, record in records.iterrows():
            result, steps = None, None
            try:
                result, steps = self.classify(record)
            except ClassificationError:
                pass

            yield result, steps, record


#     def draw_key(self, root=0):
#         """ Generate a plot of the Key """
#         #TODO - decide plotting software and implement it properly, graphviz is a pain to install and uggghhhly
# 
#         pos = graphviz_layout(self.key, prog='dot', root=self.key.node[root])
#         nx.draw(self.key, pos, with_labels=True, arrows=True)
#         plt.show()




def build_key(key_df, key_desc):
    """

    Build a NetworkX DiGraph containing couplets (nodes) joined by rules (edges)

    TODO: key couplet/class data model is nasty and a hangover from the old key_to_key and key_to_mvg model

    Args:
        key_df (pandas.DataFrame): dataframe containing the key couplets and rules
            dataframe must have the following column structure:
             - INPUT_COUPLET = unique integer identifying the parent couplet.
             - RULES = string containing expression to test.

                Expression format must be valid python syntax and conform to the following grammar:

                    `[not] rule_id [[and|or][not][rule_id]]`

                `rule_id` is an integer identifying each rule to be tested.

                Examples:

                    NNN
                    not NNN
                    NNN or NN
                    NNN or NN or N
                    not (NNN or NN)
                    (NNN or NN) or (N and NNNN)
                    NNN and not NN


             - OUTPUT_COUPLET = couplet to output if rules expression is True (mutally exclusive with OUTPUT_CLASS)
             - OUTPUT_CLASS = class to output if rules expression is True (mutally exclusive with OUTPUT_COUPLET)
             - OUTPUT_NAME = Output couplet/class name
             - COMMENTS [optional] = Additional comments
                 
        key_desc: Text description of the Key.
            Used as the description of the root node

    Returns:
        key: nx.DiGraph
    """
    key = nx.DiGraph()
    key.root = Couplet(0, 'root', key_desc)  ## Root couplet ID must always be 0
    key.add_node(key.root.id, couplet=key.root)

    for idx, row in key_df.iterrows():
        in_couplet = int(row['INPUT_COUPLET'])
        if pd.isnull(row['OUTPUT_COUPLET']):  # leaf node
            couplet = Couplet(int(row['OUTPUT_CLASS']), 'class', row['OUTPUT_NAME'], row['COMMENTS'])
        else:
            couplet = Couplet(int(row['OUTPUT_COUPLET']), 'couplet', row['OUTPUT_NAME'], row['COMMENTS'])

        key.add_node(couplet.id, couplet=couplet)
        key.add_edge(in_couplet, couplet.id, ruleset=row['RULES'])

    return key

