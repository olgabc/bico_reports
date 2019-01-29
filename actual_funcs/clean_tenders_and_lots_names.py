from libs.db_libs.load import load_some_xlsx


def clean_tenders_names(dataframe):
    """
clean tender's and lot's names
    """

    replace_patterns = load_some_xlsx("replace_names_patterns.xlsx", folder="actual_funcs")
    replace_patterns.fillna('', inplace=True)

    for f, r in zip(replace_patterns["Find"], replace_patterns["Replace"]):
        dataframe["Название тендера и лота"] = dataframe["Название тендера и лота"].str.replace(
            pat=f,
            repl=r,
            case=False
        )
    dataframe["Название тендера и лота"] = dataframe["Название тендера и лота"].str.capitalize()
    return dataframe
