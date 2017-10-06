"""
VICTA

Author:
    Luke Pinner (ERIN)

TODO:
    - Package level doc

Example::

    import pandas as pd
    from victa import Key, ClassificationError

    if __name__ == '__main__':

        ## Read couplets & rules
        ## Here we read from a spreadsheet, but you could get these from anywhere, a database, url, etc...
        ## All we need is pandas.DataFrame objects conforming to the structures documented in
        ## victa.rules.build_rules and victa.key.build_key
        ruledf = pd.read_excel(open('../data/rules_nvis.xlsx', 'rb'))
        keydf = pd.read_excel(open('../data/keys_nvis.xlsx', 'rb'))

        ## Build key
        key = Key(keydf, 'MVG Key', ruledf)

        ## Read in tha records
        ## Here we read from a spreadsheet, but you could get the data from anywhere, a database, url, etc...
        ## All we need is a pandas.DataFrame object
        recsdf = pd.read_excel(open('../data/FLATNVIS_VEG_DESC5.xlsx', 'rb'))

        ## iterate yerself
        all_results = []
        all_steps = []
        for idx, record in recsdf.iterrows():
            try:
                #Perform the classification
                result, steps = key.classify(record, id_field='NVIS_ID')
                all_results += [result]
                all_steps += [steps]
            except ClassificationError as e:
                print('Unable to classify record (NVIS_ID=%s)' % (record['NVIS_ID']))

        ## Write out the results
        all_results = pd.DataFrame(all_results)
        all_steps = pd.concat(all_steps, ignore_index=True)
        all_results.to_excel('C:/temp/mvgs_nvis_results.xlsx', index=False)
        all_steps.to_excel('C:/temp/mvgs_nvis_steps.xlsx', index=False)
"""

__all__ = ['Key', 'ClassificationError', 'Rule', 'RuleSet', 'RuleSyntaxError', 'Couplet']

from .key import Key, ClassificationError
from .rules import RuleSyntaxError, Rule, RuleSet
from .couplets import Couplet
