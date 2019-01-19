from xlsx_hyperlinks import *
from concat_xlsx_files import concat_xlsx_files_from_folder


test_file = "test_0.xlsx"
test_list = "List 1"
test_folder = "test_xlsxs"
adresses = get_hyperlinks_adresses_col(test_file, test_list, 4, test_folder)
print(len(adresses))

texts = [str(i) for i in range(1, 51)]
print(texts)

set_hyperlinlks_in_excel_col(

    hyperlinks_adresses=adresses,
    hyperlinks_texts=texts,
    xl_col=3,
    folder=test_folder,
    tip="wowowow"

)

concat_xlsx_files_from_folder("plans_customers.xlsx", test_folder)
