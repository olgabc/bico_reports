import pandas as pd


def clean_tenders_names(dataframe):
    """
clean tender's and lot's names
    """

    find_replace = pd.read_csv("replace_names_patterns.csv", delimiter=';')
    find_replace.fillna('', inplace=True)

    for f, r in zip(find_replace["Find"], find_replace["Replace"]):
        dataframe["tender_name"] = dataframe["tender_name"].str.replace(pat=f, repl=r, case=False)
        dataframe["lots_names"] = dataframe["lots_names"].str.replace(pat=f, repl=r, case=False)

    return dataframe