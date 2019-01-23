import os
import pandas as pd

from libs.db_libs.load import load_some_xlsx
from libs.db_libs.write import write_some_xlsx


def concat_xlsx_files_from_folder(path, xls_folder):
    files_list = os.listdir(xls_folder)
    df_xlsx_list = []

    for file in files_list:
        if ".xlsx" in file:
            df_xlsx = load_some_xlsx(file, xls_folder)
            df_xlsx["file_name"] = file[:-5]
            print(df_xlsx)
            df_xlsx_list.append(df_xlsx)

    df_xlsxs = pd.concat(df_xlsx_list, ignore_index=True)
    write_some_xlsx(df_xlsxs, path, "")
