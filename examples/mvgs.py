import os
import pandas as pd
from victa import Key, ClassificationError, MultipleMatchesError

if __name__ == '__main__':

    id_field = 'NVIS_ID'

    output_results = '../data/mvgs_nvis_results.xlsx'
    output_steps = '../data/mvgs_nvis_steps.xlsx'

    for output in (output_results, output_steps):
        if os.path.exists(output):
            os.unlink(output)


    # Read couplets & rules
    # Here we read from a spreadsheet, but you could get these from anywhere,
    # a database, url, etc...
    # All we need is pandas.DataFrame objects conforming to the structures
    # documented in victa.rules.build_rules and victa.key.build_key
    ruledf = pd.read_excel(open('../data/rules_nvis.xlsx', 'rb'))
    keydf = pd.read_excel(open('../data/keys_nvis.xlsx', 'rb'))

    # Build key
    key = Key(keydf, 'MVG Key', ruledf)

    # Read in tha records
    # Here we read from a spreadsheet, but you could get the data from anywhere,
    # a database, url, etc... All we need is a pandas.DataFrame object
    recsdf = pd.read_excel(open('../data/FLATNVIS_VEG_DESC5.xlsx', 'rb'))

    # iterate yerself
    all_results = []
    all_steps = []
    for idx, record in recsdf.iterrows():
        try:
            # Perform the classification
            result, steps = key.classify(record, id_field=id_field)
            all_results += [result]
            all_steps += [steps]
        except ClassificationError as e:
            print(e)
            # Can also do something with e.record and e.steps
        except MultipleMatchesError as e:
            print(e)
            # Can also do something with e.record, e.couplet and e.rulesets

    # Write out the results
    all_results = pd.DataFrame(all_results)
    all_steps = pd.concat(all_steps, ignore_index=True)
    all_results.to_excel(output_results, index=False)
    all_steps.to_excel(output_steps, index=False)
