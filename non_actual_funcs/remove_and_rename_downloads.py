import os


def get_folders_from_folder(folder):
    items = os.listdir(folder)
    folder_names = []
    for item in items:
        if "." not in item:
            folder_names.append(item)

    return folder_names


def get_files_from_folder(folder):
    items = os.listdir(folder)
    file_names = []
    for item in items:
        if "." in item:
            file_names.append(item)

    return file_names


def remove_and_rename_files(main_folder):
    main_path = os.path.abspath(main_folder)
    folders = get_folders_from_folder(main_folder)

    for folder in folders:
        folder_path = os.path.join(main_path, folder)
        files = get_files_from_folder(os.path.join(main_folder, folder))

        for file in files:
            file_index = files.index(file) + 1
            file_path = os.path.join(folder_path, file)
            file_name, file_ext = os.path.splitext(file_path)
            new_name = "{}_{}{}".format(folder, file_index, file_ext)
            new_path = os.path.join(main_path, new_name)
            os.rename(file_path, new_path)

        os.rmdir(folder_path)


remove_and_rename_files("test_xlsx")
