import pandas as pd
from libs.db_libs.write import write_some_xlsx
#import requests
import re


my_link = """
http://www.bicotender.ru/crm/analytics/list/?region_id[0]=2774&multiregions=0&field_id[0]=1070&multifields=0&search_by_lots=1&search_by_positions=1&earlierDate[from]=2015-01-01&earlierDate[to]=2015-12-31&finalCost[from]=1&status_id[0]=4&status_id[1]=5&status_id[2]=6&status_id[3]=7&caption=%D0%97%D0%B0%D0%BA%D1%83%D0%BF%D0%BA%D0%B8%20%D0%B2%20%D0%B2%D0%B0%D1%88%D0%B5%D0%BC%20%D1%80%D0%B5%D0%B3%D0%B8%D0%BE%D0%BD%D0%B5&atype=field_1&showConf[asLot]=2&showConf[competitorFilterMode]=2&submit=1
"""

download_link = r'D:\bico_reports\html_downloads\Закупки в вашем регионе - копия.html'


def generate_link(link, page_num=1, on_page=500):
    link = link.replace("/list/", "/list/page/{}/".format(page_num))
    link = link.replace("#{%22tab%22:%22tab-general%22}", "")
    link = link.replace("&on_page=50", "&on_page={}".format(on_page))
    return link


def download_html(link_example, results_qty, on_page=500, folder="html_files"):
    pages_qty = int(results_qty / on_page) + 1
    pages = [i for i in range(1, pages_qty + 1)]
    dataframes = []

    for page in pages:
        download_html


def replace_html_text(html_path):

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

    table_rows = re.findall(r'<tr(.+?)</tr>+?', filedata)

    for row in table_rows:

        new_row = row
        row_cells = re.findall(r'<td(.+?)</td>+?', row)
        len_row = len(row_cells)

        cols = []

        if len_row == 21:
            cols = [14, 15, 17]

        elif len_row == 4:
            cols = [0]

        rowspan = 1
        rowspans = re.findall(r'style="width:70px; "rowspan="(.+?)"+?', row)

        if rowspans:
            rowspan = rowspans[0]

        for col_num in cols:
            link = ""
            try:
                link = re.findall(r'/crm/company/details/company_id/(.+?)/+?', row_cells[col_num])[0]
                link = r'https://www.bicotender.ru/crm/company/details/company_id/{}/?submit=1'.format(
                    link
                )
                print(rowspan, col_num, "link", link)

            except IndexError:
                print(col_num, "WWW_link", link)

            if col_num == 17:
                rowspan = 1

            new_row += r'<td style="width:150px; "rowspan="{0}" class="text-align-right" data-order-value="{1}">{1}</td>'.format(
                rowspan,
                link
            )

        filedata = filedata.replace(row, new_row)

    with open(html_path, 'w', encoding='utf-8') as file:
        file.write(filedata)


def parse_tables_from_folder(html_path):
    tables = pd.read_html(html_path)
    print(tables[3])
    return tables[3]

replace_html_text(download_link)
#xls = parse_tables_from_folder(download_link)
#write_some_xlsx(xls, "html_table.xlsx", index=True)
