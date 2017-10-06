import pandas as pd
from victa import Key, ClassificationError

if __name__ == '__main__':

    ## Read couplets & rules
    ruledf = pd.read_excel(open('../data/rules_nvis.xlsx','rb'))
    keydf = pd.read_excel(open('../data/keys_nvis.xlsx', 'rb'))

    ## Build key
    key = Key(keydf, 'MVG Key', ruledf)

    ## Read in tha records
    recsdf = pd.read_excel(open('../data/FLATNVIS_VEG_DESC5.xlsx', 'rb'))

    ## iterate yerself
    all_results = []
    all_steps = []
    for idx, record in recsdf.iterrows():
        try:
            result, steps = key.classify(record)
            result.loc['NVIS_ID'] = record['NVIS_ID'] #Series
            steps = steps.assign(NVIS_ID=record['NVIS_ID']) #Datafeame
            all_results += [result]
            all_steps += [steps]
        except ClassificationError as e:
            print('Unable to classify record (NVIS_ID=%s)' % (record['NVIS_ID']))

    all_results = pd.DataFrame(all_results)
    all_steps = pd.concat(all_steps, ignore_index=True)
    all_results.to_excel('C:/temp/mvgs_nvis_results.xlsx', index=False)
    all_steps.to_excel('C:/temp/mvgs_nvis_steps.xlsx', index=False)
