import os
import pandas as pd


def write_some_csv(some_dataframe, name, folder):
    file_path = os.path.join(
        folder,
        name
    )

    some_dataframe.to_csv(
        file_path,
        encoding="cp1251",
        index=False,
        sep=";"
    )


def write_some_xlsx(some_dataframe, name, folder="", index=False):
    file_path = os.path.join(
        folder,
        name
    )

    writer = pd.ExcelWriter(file_path)
    some_dataframe.to_excel(writer, 'List 1', index=index)
    writer.save()
