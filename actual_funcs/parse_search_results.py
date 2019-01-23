import pandas as pd
from libs.db_libs.write import write_some_xlsx
import requests
import re
import os
from config.config import DATA_PARAM


my_link = """
https://www.bicotender.ru/crm/analytics/list/?region_id[0]=2774&multiregions=0&field_id[0]=1070&multifields=0&search_by_lots=1&search_by_positions=1&earlierDate[from]=2018-01-01&earlierDate[to]=2018-12-31&finalCost[from]=1&status_id[0]=4&status_id[1]=5&status_id[2]=6&status_id[3]=7&caption=%D0%97%D0%B0%D0%BA%D1%83%D0%BF%D0%BA%D0%B8%20%D0%B2%20%D0%B2%D0%B0%D1%88%D0%B5%D0%BC%20%D1%80%D0%B5%D0%B3%D0%B8%D0%BE%D0%BD%D0%B5&atype=field_1&showConf[asLot]=2&showConf[competitorFilterMode]=2&submit=1
"""


def generate_link(link, page_num=1, on_page=500):
    link = link.replace("/list/", "/list/page/{}/".format(page_num))
    link = link.replace("#{%22tab%22:%22tab-general%22}", "")
    link = link.replace("&on_page=50", "&on_page={}".format(on_page))
    return link


def download_html(link_example, results_qty, on_page=500, folder="html_downloads"):
    pages_qty = int(results_qty / on_page) + 1
    page_nums = [i for i in range(1, pages_qty + 1)]

    for page_num in page_nums:
        page_link = generate_link(link=link_example, page_num=page_num, on_page=on_page)
        p = requests.post(page_link, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=DATA_PARAM)
        page_path = os.path.join(folder, "{}.html".format(page_num))

        with open(page_path, 'w', encoding='utf-8') as file:
            file.write(p.text)


def get_replaced_html_text(html_path):

    with open(html_path, 'r', encoding='utf-8') as file:
        filedata = file.read()

    filedata = filedata.replace(
        r'<th style="width:150px; ">Контракт</th>',
        r'<th style="width:150px; ">Контракт</th><th style="width:150px; ">Ссылка на заказчика</th><th style="width:150px; ">Ссылка на поставщика</th><th style="width:150px; ">Ссылки на участников</th>'
    )
    filedata = filedata.replace(
        r'<th style="width:150px; ">20</th>',
        r'<th style="width:150px; ">20</th><th style="width:150px; ">21</th><th style="width:150px; ">22</th><th style="width:150px; ">23</th>'
    )

    filedata = filedata.replace(
        r'<th style="width:150px; ">20</th>',
        r'<th style="width:150px; ">20</th><th style="width:150px; ">21</th><th style="width:150px; ">22</th><th style="width:150px; ">23</th>'
    )

    table_rows = re.findall(r'<tr(.+?)</tr>+?', filedata)

    for row in table_rows:

        new_row = row
        row_cells = re.findall(r'<td(.+?)</td>+?', row)
        len_row = len(row_cells)

        cols = []

        if len_row == 21:
            cols = [14, 15, 17]

        for col_num in cols:
            link = ""
            try:
                link = re.findall(r'/crm/company/details/company_id/(.+?)/+?', row_cells[col_num])[0]
                link = r'https://www.bicotender.ru/crm/company/details/company_id/{}/?submit=1'.format(
                    link
                )

            except IndexError:
                pass

            new_row += r'<td style="width:150px; "rowspan="1" class="text-align-right" data-order-value="{0}">{0}</td>'.format(
                link
            )

        filedata = filedata.replace(row, new_row)

    return filedata


def parse_html_tables_from_folder(folder, no_participants=True):
    html_files = [os.path.join(folder, html_file) for html_file in os.listdir(folder) if ".html" in html_file]
    tables = []

    for html_file in html_files:
        tables.append(pd.read_html(get_replaced_html_text(html_file))[3])

    concat_tables = pd.concat(tables, ignore_index=True)
    cols = [col[0] for col in concat_tables.columns]

    if no_participants:
        concat_tables.dropna(thresh=7, inplace=True)
        concat_tables.drop(cols[23:], axis=1, inplace=True)
        concat_tables.drop(cols[17:20], axis=1, inplace=True)

    concat_tables.drop(["#", "Названия позиций"], axis=1, inplace=True)
    index = range(1, len(concat_tables) + 1)
    concat_tables.index = index
    concat_tables.index.names = ["#"]

    float_cols = ["Сумма НМЦК", "Предложенная цена", "Снижение, %"]

    for float_col in float_cols:
        concat_tables[float_col] = concat_tables[float_col].replace(regex=r'[\s.]|(RUR)', value="")

    return concat_tables


download_html(my_link, results_qty=10)
xls = parse_html_tables_from_folder("html_downloads")
print(xls)
write_some_xlsx(xls, "html_table.xlsx", index=True)
