from pandas import merge as pd_merge
from math import isnan


def duplicates_have_different_sources(x):
    return x['min'] != x['max']


def original_or_copy(x):
    if isnan(x['duplicates_have_different_sources']):
        return

    else:
        if x['Робот'] in ["2000", "5000", "5100"]:
            return "original"
        else:
            return "copy"


def mark_duplicates(dataframe):

    dataframe["is_duplicate"] = dataframe.duplicated(
        subset=["Название тендера и лота", "Опубликован", "Сумма НЦК"],
        keep=False
    )
    dataframe_duplicates = dataframe.loc[
        dataframe["is_duplicate"],
        ["Название тендера и лота", "Опубликован", "Сумма НЦК", "Робот"]
    ]

    gb = dataframe_duplicates.groupby(
        ["Название тендера и лота", "Опубликован", "Сумма НЦК"],
    ).aggregate(min)

    gb = gb.rename(index=str, columns={"Робот": "min"})
    gb["max"] = dataframe_duplicates.groupby(["Название тендера и лота", "Опубликован", "Сумма НЦК"])['Робот'].max()
    gb["duplicates_have_different_sources"] = gb.apply(duplicates_have_different_sources, axis=1)
    gb = gb[gb["duplicates_have_different_sources"]]
    gb = gb.reset_index()
    dataframe = pd_merge(
        dataframe,
        gb,
        on=["Название тендера и лота", "Опубликован", "Сумма НЦК"],
        how='left'
    )
    dataframe["original_or_copy"] = dataframe.apply(
        original_or_copy,
        axis=1
    )
    dataframe.drop
    return dataframe
