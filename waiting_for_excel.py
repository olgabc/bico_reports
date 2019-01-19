import os
import pandas as pd
import subprocess


def reset_all_changes(category):
    """
revert csv_file for category chosen to initial condition from initial excel_file, delete update file
    """

    category_frame = pd.read_excel(
        "data/initial_data/{}.xls".format(category),
        sheet_name=0,
        keep_default_na=False,
        parse_dates=['start_date']
    )
    category_frame.index = category_frame["#"]
    category_frame.drop("#", axis=1, inplace=True)
    category_frame["category"] = category
    category_frame["sub_category"] = category
    category_frame["is_checked"] = "no"
    category_frame.replace("^-$", '', regex=True, inplace=True)
    category_frame["declined_qty"] = category_frame[["tender_status", "declined_qty", "players_qty"]].apply(
        lambda x: "" if x["tender_status"] == "" and x["players_qty"] == "" else x["declined_qty"],
        axis=1
    )

    category_frame.to_csv(
        "data/edited_data/{}.csv".format(category),
        sep=";",
        encoding="cp1251"
    )

    update_names = [
        "data/edited_data/update_lots_{}.csv".format(category),
        "data/edited_data/update_tenders_{}.csv".format(category)
    ]

    for update_name in update_names:
        if os.path.exists(update_name):
            os.remove(update_name)


def load_some_data(some_data, parsed_dates=False, cols=None):
    """
returns DataFrame
    """

    some_frame = pd.read_csv(
        some_data,
        encoding="cp1251",
        sep=";",
        keep_default_na=False,
        parse_dates=parsed_dates,
        usecols=cols
    )
    some_frame.index = some_frame["#"]
    some_frame.drop("#", axis=1, inplace=True)

    for col in some_frame.select_dtypes(exclude="datetime"):
        some_frame[col] = some_frame[col].apply(lambda x: str(x))

    return some_frame


def load_category_data(category, parsed_dates="default", cols=None):
    """
returnes data for chosen category as DataFrame object
    """

    some_data = "data/edited_data/{}.csv".format(category)

    if parsed_dates == "default":
        parsed_dates = ['start_date']
    elif parsed_dates == "":
        parsed_dates = False

    category_frame = load_some_data(
        some_data=some_data,
        parsed_dates=parsed_dates,
        cols=cols
    )
    return category_frame


def load_category_update(category, tenders_or_lots):
    """
returns update for chosen category as DataFrame object, tenders_or_lots takes values: "tenders" or"lots"
    """

    some_data = "data/edited_data/update_{}_{}.csv".format(tenders_or_lots, category)

    update_frame = load_some_data(some_data=some_data)
    return update_frame


def count_checked_qty(frame):
    frame.rename(
        columns={"tender_id": "count"},
        inplace=True
    )
    results = frame.pivot_table(
        values="count",
        index="is_checked",
        aggfunc="count"
    )
    print(
        """
{}

total_rows: 
{}
        """.format(results, len(frame.index))
    )


def update_lots_data(category, show_checked_qty=True):
    update_name = "data/edited_data/update_lots_{}.csv".format(category)

    if not os.path.exists(update_name):
        return

    category_frame = load_category_data(category)
    update_frame = load_category_update(category, "lots")

    category_frame.update(update_frame)

    category_frame.to_csv(
        "data/edited_data/{}.csv".format(category),
        encoding="cp1251",
        sep=";"
    )

    os.remove(update_name)

    if show_checked_qty:
        count_checked_qty(category_frame)


def update_tenders_data(category, show_checked_qty=True):
    """
mark tenders as duplicates from tender duplicates request file   
    """

    update_name = "data/edited_data/update_tenders_{}.csv".format(category)

    if not os.path.exists(update_name):
        return

    category_frame = load_category_data(category)
    update_frame = load_category_update(category, "tenders")

    joined_frame = category_frame.merge(update_frame, how='left', on=["tender_id"], suffixes=("", "_update"))
    joined_frame.index = category_frame.index
    joined_update_frame = joined_frame["tender_id"].to_frame()

    cols = list(joined_frame)
    for col in cols:
        if col[-7:] == '_update':
            joined_update_frame[col[:-7]] = joined_frame[col]

    category_frame.update(joined_update_frame)

    category_frame.to_csv(
        "data/edited_data/{}.csv".format(category),
        encoding="cp1251",
        sep=";"
    )
    os.remove(update_name)

    if show_checked_qty:
        count_checked_qty(category_frame)


def update_all_data(category):
    update_lots_data(category)
    update_tenders_data(category)


def get_duplicates_request(category):
    """
creates csv with tenders, which are probably duplicates
    """

    update_all_data(category)

    cols = [
        "#",
        "tender_id",
        "tender_name",
        "tender_cost",
        "start_date",
        "tender_type",
        "customer",
        "robot_id",
        "is_checked"
    ]
    duplicates_frame = load_category_data(category, cols=cols)
    duplicates_frame["duplicated_name"] = duplicates_frame.duplicated("tender_name", keep=False)
    duplicates_frame["duplicated_cost"] = duplicates_frame.duplicated("tender_cost", keep=False)
    duplicates_frame = duplicates_frame.loc[
        (duplicates_frame["duplicated_name"] == True) &
        (duplicates_frame["duplicated_cost"] == True)
        ]
    duplicates_frame.drop(["duplicated_name", "duplicated_cost"], axis=1, inplace=True)
    duplicates_frame.drop_duplicates("tender_id", inplace=True)
    duplicates_frame = duplicates_frame.loc[duplicates_frame["is_checked"] == "no"]

    if not len(duplicates_frame.index):
        print("""request returnes nothing or rows was checked""")
        return

    duplicates_frame["is_checked"] = duplicates_frame[["robot_id"]].apply(
        lambda x: "checked" if x["robot_id"] in [5000, 2000, 5100] else "duplicate",
        axis=1
    )

    duplicates_frame.sort_values(
        by=["tender_cost", "start_date", "tender_name"],
        axis=0,
        inplace=True
    )

    update_name = "data/edited_data/update_tenders_{}.csv".format(category)
    duplicates_frame.to_csv(
        update_name,
        encoding="cp1251",
        sep=";"
    )

    subprocess.Popen(
        ["start", update_name],
        shell=True
    )


def get_names_request(category, request='', find_in="tender_name"):
    """
find patterns in names, "find_in" takes values: "tender_name", "lot_name", "lot_positions_names"
    """

    update_all_data(category)

    cols = [
        "#",
        "tender_id",
        "lot_id",
        "tender_name",
        "lot_name",
        "lot_positions_names",
        "lot_cost",
        "category",
        "sub_category",
        "is_checked"

    ]
    request_frame = load_category_data(category, parsed_dates='', cols=cols)
    request_frame["match"] = request_frame[find_in].str.contains(pat=request, case=False)
    request_frame = request_frame.loc[request_frame["match"].values]
    request_frame = request_frame.loc[request_frame["is_checked"] == "no"]

    if not len(request_frame.index):
        print("request returnes nothing or rows was checked")
        return

    request_frame.drop("match", axis=1, inplace=True)

    update_name = "data/edited_data/update_lots_{}.csv".format(category)
    request_frame.to_csv(
        update_name,
        encoding="cp1251",
        sep=";"
    )

    subprocess.Popen(
        ["start", update_name],
        shell=True
    )


