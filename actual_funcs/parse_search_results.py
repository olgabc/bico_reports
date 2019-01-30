import pandas as pd
import requests
import re
import os
from config.config import DATA_PARAM, project_folder


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
        page_path = os.path.join(project_folder, folder, "{}.html".format(page_num))

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
        long_row = row
        row_cells = re.findall(r'<td(.+?)</td>+?', row)
        len_row = len(row_cells)

        cols = []

        if len_row == 21:

            cell_text = re.search("' target='_blank'>(.*)(?=</b)", row_cells[3])
            tooltip_text = re.search(r'Tooltip" title="(.*)(?=<a href)', row_cells[3])

            if cell_text and tooltip_text:
                long_row = row.replace(
                    cell_text[0].replace("' target='_blank'>", ''),
                    tooltip_text[0].replace('Tooltip" title="', '')
                )

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
        filedata = filedata.replace(row, long_row)

    return filedata


def parse_html_tables_from_folder(folder):
    html_files = [
        os.path.join(
            project_folder,
            folder,
            html_file
        ) for html_file in os.listdir(
            os.path.join(
                project_folder,
                folder
            )
        ) if ".html" in html_file
    ]

    tables = []

    for html_file in html_files:
        tables.append(pd.read_html(get_replaced_html_text(html_file))[3])

    concat_tables = pd.concat(tables, ignore_index=True)
    concat_tables.columns = concat_tables.columns.droplevel(1)
    return concat_tables


def set_link_and_robot_id(source):
    robot = re.search(r'robot(\d+)', source)[0]
    links = source.replace(robot, "")
    many_links = re.search(r'(.+)(?=http)', links)

    if many_links:
        link = many_links[0]
    else:
        link = links

    return {"link": link, "robot": robot.replace("robot", "")}


def beatify_parsed_tables(dataframe, no_participants=True):

    if no_participants:
        dataframe.dropna(thresh=7, inplace=True)
        dataframe.drop(dataframe.columns[23:], axis=1, inplace=True)
        dataframe.drop(dataframe.columns[17:20], axis=1, inplace=True)

    dataframe.drop(["#", "Названия позиций", "Контракт"], axis=1, inplace=True)

    index = range(1, len(dataframe) + 1)
    dataframe.index = index
    dataframe.index.names = ["#"]

    float_cols = ["Сумма НМЦК", "Предложенная цена", "Снижение, %"]

    for float_col in float_cols:
        dataframe[float_col] = dataframe[float_col].replace(regex=r'[\s]|(RUR)', value="")
        dataframe[float_col] = dataframe[float_col].replace(regex=r'\.', value=",")

    dataframe["Название тендера и лота"] = dataframe["Название тендера и лота"].replace(regex=r'>', value="")

    dataframe["Робот"] = dataframe["Источник"].apply(lambda x: set_link_and_robot_id(x)["robot"])
    dataframe["Источник"] = dataframe["Источник"].apply(lambda x: set_link_and_robot_id(x)["link"])

    dataframe = dataframe.rename(index=str, columns={"Сумма НМЦК": "Сумма НЦК"})
    dataframe["Название тендера и лота"] = dataframe["Название тендера и лота"].str.capitalize()

    return dataframe
