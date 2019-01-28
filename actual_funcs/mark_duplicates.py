def title_cost(x,y):
    if x:
        if y in [2000, 5000, 5100]:
            return "original"
        else:
            return "copy"
    else:
        return x


def wrapper(x):
    return title_cost(x['duplicates'], x['Робот'])


def mark_duplicates(dataframe):
    dataframe["Название тендера и лота"] = dataframe["Название тендера и лота"].str.capitalize()
    dataframe["duplicates"] = dataframe.duplicated(
        subset=["Название тендера и лота", "Опубликован", "Сумма НЦК"],
        keep=False
    )
    dataframe_duplicates = dataframe[dataframe["duplicates"]]
    dataframe_duplicates["duplicates"] = dataframe_duplicates["Робот"].apply()
    dataframe["duplicates"] = dataframe[["duplicates", "Робот"]].apply(wrapper, axis=1)
    print(dataframe_duplicates["duplicates"])
    return dataframe
