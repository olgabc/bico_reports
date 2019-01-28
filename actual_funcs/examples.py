import os
from actual_funcs.parse_search_results import download_html, parse_html_tables_from_folder, \
    beatify_parsed_tables
from libs.db_libs.write import write_some_xlsx
from actual_funcs.clean_tenders_and_lots_names import clean_tenders_names
from config.config import project_folder
from libs.db_libs.load import load_some_xlsx
from actual_funcs.mark_duplicates import mark_duplicates
import re

my_link = """
https://www.bicotender.ru/crm/analytics/list/?region_id[0]=2774&multiregions=0&field_id[0]=1070&multifields=0&search_by_lots=1&search_by_positions=1&earlierDate[from]=2018-01-01&earlierDate[to]=2018-12-31&finalCost[from]=1&status_id[0]=4&status_id[1]=5&status_id[2]=6&status_id[3]=7&caption=%D0%97%D0%B0%D0%BA%D1%83%D0%BF%D0%BA%D0%B8%20%D0%B2%20%D0%B2%D0%B0%D1%88%D0%B5%D0%BC%20%D1%80%D0%B5%D0%B3%D0%B8%D0%BE%D0%BD%D0%B5&atype=field_1&showConf[asLot]=2&showConf[competitorFilterMode]=2&submit=1
"""

"""
download_html(my_link, results_qty=3200)
parsed_df = parse_html_tables_from_folder("html_downloads")
write_some_xlsx(parsed_df, os.path.join(project_folder, "parsed.xlsx"), index=True)
"""

cleaned_names_df = load_some_xlsx("cleaned_names.xlsx", folder="")
#beatified_df = beatify_parsed_tables(cleaned_names_df)
marked_duplicates = mark_duplicates(cleaned_names_df)
#write_some_xlsx(marked_duplicates, os.path.join(project_folder, "marked_duplicates.xlsx"), index=True)

#cleaned_names_df = load_some_xlsx("cleaned_names.xlsx", folder="")
