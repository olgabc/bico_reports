import pandas as pd


def clean_tenders_names(dataframe):
    """
clean tender's and lot's names
    """

    replace_patterns = pd.read_csv("replace_names_patterns.csv", delimiter=';')
    replace_patterns.fillna('', inplace=True)

    for f, r in zip(replace_patterns["Find"], replace_patterns["Replace"]):
        dataframe["Название тендера и лота"] = dataframe["Название тендера и лота"].str.replace(pat=f, repl=r, case=False)

    return dataframe
