# Vegetation Information Classification Tool Automator (VICTA) core library

This is a minimal implementation of a core library that can be built on to develop a new VICTA application.

## Contents
 - [Introduction](#introduction)
 - [Data Model](#data-model)
     * [Key](#key)
     * [Rules](#rules)
 - [Code Example](#code-example)
 - [Installation](#installation)
 - [API Reference](#api-reference)
 - [Tests](#tests)
 - [Contributors](#contributors)
 - [License](#license)

## Introduction
The VICTA core library consists of a classification key built from a [directed graph](https://en.wikipedia.org/wiki/Directed_graph) ([NetworkX DiGraph](https://networkx.github.io/documentation/stable/reference/classes/digraph.html)). The key is constructed from a set of couplets (graph nodes) and associated rules (graph edges).  The classification key exposes a well defined API for passing data, key and rule logic in, requesting the classification of a data record, the decision path of that classification and the reporting of application exception and validation errors.  There is no business logic hard-coded into the core library, it is a business/data agnostic decision tree only.

A simple diagram of the minimal implemented core library:

    +------------------------------------------------+
    |Command line script/GUI/Web App/Jupyter Notebook|
    |                                                |
    |    +-----------------+  +------------------+   |
    |    |     INPUTS      |  |     OUTPUTS      |   |
    |    | Data/Rules/Keys |  | Classification   |   |
    |    |                 |  | Decision path    |   |
    |    +--------------+--+  +--^---------------+   |
    |                   |        |                   |
    |            +------v--------+-------+           |
    |            |        CORE API       |           |
    |            |  Classification Tree  |           |
    |            |  Rule and Key parsers |           |
    |            +-----------------------+           |
    +------------------------------------------------+

## Data Model
The key (couplets) and rules are passed in as [Pandas DataFrames](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html), a tabular/iterable in-memory data structure. The exact format is similar to the existing "Key to Key" and "Key to MVG" format, but merged to a single table.

### Key
The key dataframe must have the following column structure:

| Attribute Name  | Description                                                                         |
|-----------------|-------------------------------------------------------------------------------------|
| INPUT_COUPLET   | Unique integer identifying the parent couplet.                                      |
| RULES           | String containing expression** to test.                                             |
| OUTPUT_COUPLET  | Couplet to output if rules expression is True (mutally exclusive with OUTPUT_CLASS) |
| OUTPUT_CLASS    | Class to output if rules expression is True (mutally exclusive with OUTPUT_COUPLET) |
| OUTPUT_NAME     | Output couplet/class name                                                           |
| COMMENTS        | Additional comments [optional]                                                      |


>** The RULES expression format must be valid python syntax and conform to the following grammar:
>
>     [not] rule_id [[and|or][not][rule_id]]
>
> Where: `rule_id` is an integer identifying each rule to be tested.
>
>Examples:
>
>     NNN
>     not NNN
>     NNN or NN
>     NNN or NN or N
>     not (NNN or NN)
>     (NNN or NN) or (N and NNNN)
>     NNN and not NN

### Rules
The rules dataframe must have the following column structure:

| Attribute Name  | Description                          |
|-----------------|--------------------------------------|
| ID              | Unique integer identifying the rule. |
| ATTRIBUTE       | Attribute/column to use when rule is tested (i.e. in the record to be classified by the key)|
| OPERATOR        | Positive comparison operator: `in`, `=`, `>=`, `>`, `<=`, `<`, `regex`  (where: `regex` is a valid [regular expression](https://docs.python.org/3/library/re.html) )|
| VALUE           | Text string to look for in ATTRIBUTE |
| NAME            | Rule name                            |
| COMMENTS        | Additional comments [optional]       |


## Code Example

~~~~ {#example .python .numberLines startFrom="1"}
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

~~~~

## Installation

    conda-env create -f victa.yml
    activate victa

## API Reference

https://victa.readthedocs.io/en/latest/

## Tests

Some basic tests of rules started. Needs more test coverage.

## Contributors

Luke Pinner

## License
Apache 2.0