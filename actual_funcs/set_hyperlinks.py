import os
from string import ascii_uppercase as alphabet
import xlsxwriter
from config.config import project_folder

excel_cols = []

for letter in alphabet:
    excel_cols.append(letter)

for first_letter in alphabet:
    for second_letter in alphabet:
        excel_cols.append(first_letter + second_letter)

for first_letter in alphabet:
    for second_letter in alphabet:
        for third_letter in alphabet:
            excel_cols.append(first_letter + second_letter + third_letter)

excel_cols_dict = {i+1: excel_cols[i] for i in range(len(excel_cols))}


def set_hyperlinlks_in_excel_col(
    hyperlinks_adresses,
    hyperlinks_texts=None,
    xl_col=None,
    tip="",
    preffix="",
    xls_file="hyperlinks.xlsx",
    xls_worksheet="hyperlinks",
    folder="",
):
    """
    :param hyperlinks_adresses:
    :param hyperlinks_texts:
    :param xl_col:
    :param tip:
    :param preffix:
    :param xls_file:
    :param xls_worksheet:
    :param folder:
    :return: None
    """
    max_row = len(hyperlinks_adresses) + 1

    if not hyperlinks_texts:
        hyperlinks_texts = hyperlinks_adresses

    if preffix:
        hyperlinks_adresses = ["{}/{}/".format(preffix, hyperlink_adress) for hyperlink_adress in hyperlinks_adresses]

    xls_file_path = os.path.abspath(os.path.join(project_folder, folder, xls_file))
    workbook = xlsxwriter.Workbook(xls_file_path)
    worksheet = workbook.add_worksheet(xls_worksheet)

    for xl_row, link_adress, link_text in zip(range(1, max_row), hyperlinks_adresses, hyperlinks_texts):
        print("link:", link_adress, "text:", link_text)
        worksheet.write_url(
            row=xl_row,
            col=xl_col,
            url=link_adress,
            string=link_text,
            tip=tip
        )

    workbook.close()
