import os
import pandas as pd
from config.config import project_folder


def write_some_csv(dataframe, name, folder):
    file_path = os.path.join(
        project_folder,
        folder,
        name
    )

    dataframe.to_csv(
        file_path,
        encoding="cp1251",
        index=False,
        sep=";"
    )


def write_some_xlsx(dataframe, name, folder="", index=False):
    file_path = os.path.join(
        project_folder,
        folder,
        name
    )

    writer = pd.ExcelWriter(file_path)
    dataframe.to_excel(writer, 'List 1', index=index)
    writer.save()
