import os
from actual_funcs.parse_search_results import download_html, parse_html_tables_from_folder, \
    beatify_parsed_tables
from libs.db_libs.write import write_some_xlsx
from actual_funcs.clean_tenders_and_lots_names import clean_tenders_names
from config.config import project_folder
from actual_funcs.mark_duplicates import mark_duplicates
from libs.db_libs.load import load_some_xlsx

my_link = """
https://www.bicotender.ru/crm/analytics/list/?atype=field_1&filter_id=302437&competitorRowNumber[to]=1&showConf[asLot]=2&showConf[competitorFilterMode]=2&submit=1
"""

download_html(my_link, results_qty=4000)
parsed_df = parse_html_tables_from_folder("html_downloads")
beatyfied_df = beatify_parsed_tables(parsed_df)
cleaned_names_df = clean_tenders_names(beatyfied_df)
marked_duplicates = mark_duplicates(cleaned_names_df)
write_some_xlsx(marked_duplicates, os.path.join(project_folder, "marked_duplicates.xlsx"), index=True)
print(load_some_xlsx("marked_duplicates.xlsx", ""))