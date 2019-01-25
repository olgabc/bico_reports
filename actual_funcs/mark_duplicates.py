import pandas as pd
from libs.db_libs.load import load_some_xlsx
from libs.db_libs.write import write_some_xlsx


def mark_duplicates(name="html_table.xlsx", folder=""):
    dataframe = load_some_xlsx(name=name, folder=folder)
    dataframe["duplicated_name"] = dataframe.duplicated(subset=["Название тендера и лота", "Сумма НМЦК"], keep=False)
    print(dataframe)

mark_duplicates()