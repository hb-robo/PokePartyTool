import pandas as pd

# open basic typing .csv and convert to dictionary
types = pd.read_csv('data/gen2-5types.csv')
types = types.set_index('off_type')

# expand dictionary to include dual-typings
alltypes = types.copy()

for type1 in types:
    for type2 in types:
        if type1 == type2:
            continue

        newcol = "vs_%s_%s" % (type1.replace('vs_', ''), type2.replace('vs_', ''))

        if newcol not in alltypes.columns:
            alltypes[newcol] = ""

        for index, row in alltypes.iterrows():
            print(index)
            alltypes.at[index, newcol] = float(alltypes.at[index, type1]) * float(alltypes.at[index, type2])

alltypes.to_csv('gens2-5types_expanded.csv')
