import pandas as pd
from libs.db_libs.load import load_some_xlsx
from actual_funcs.set_hyperlinks import set_hyperlinlks_in_excel_col

xls = load_some_xlsx("с регионами.xlsx", "")

links_adresses = xls["Ссылка на поставщика"].tolist()
links_texts = xls["Победитель"].tolist()
for i in links_adresses: print(i)
set_hyperlinlks_in_excel_col(
    hyperlinks_adresses=links_adresses,
    hyperlinks_texts=links_texts,
    #preffix="https://www.bicotender.ru/tc/tender/show/tender_id/",
    xl_col=1,
    xls_file="winner_hyper_links.xlsx"
)