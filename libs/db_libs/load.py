import os
import pandas as pd
from config.config import project_folder


def load_some_xlsx(name, folder, index_col=None):
    file_path = os.path.join(
        project_folder,
        folder,
        name
    )

    some_dataframe = pd.read_excel(
        file_path,
        encoding="cp1251",
        sep=";",
        index_col=index_col
    )
    return some_dataframe


def load_some_csv(name, folder):
    file_path = os.path.join(
        project_folder,
        folder,
        name
    )

    some_dataframe = pd.read_csv(
        file_path,
        encoding="cp1251",
        sep=";",
        engine="python"
    )
    return some_dataframe
