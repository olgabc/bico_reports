from non_actual_funcs.concat_xlsx_files import concat_xlsx_files_from_folder
from libs.db_libs.write import write_some_xlsx
from libs.db_libs.load import load_some_xlsx

#cnct = concat_xlsx_files_from_folder("test_xlsxs")
#write_some_xlsx(cnct, "plans_new.xlsx")
from actual_funcs.set_hyperlinks import set_hyperlinlks_in_excel_col

hyperlinks_adresses = load_some_xlsx("планы.xlsx", folder="")["Номер тендера в системе бикотендер"].tolist()
hyperlinks_adresses = [str(adr) for adr in hyperlinks_adresses]

set_hyperlinlks_in_excel_col(
    hyperlinks_adresses,
    hyperlinks_texts=None,
    xl_col=1,
    tip="",
    preffix="http://www.bicotender.ru/tc/tender/show/tender_id/",
    xls_file="hyperlinks.xlsx",
    xls_worksheet="hyperlinks",
    folder="",
)