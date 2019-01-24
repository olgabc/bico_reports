import os
from config.config import project_folder

def get_folders_from_folder(folder):
    items = os.listdir(os.path.abspath(os.path.join(project_folder, folder)))
    folder_names = []
    for item in items:
        if "." not in item:
            folder_names.append(item)

    return folder_names


def get_files_from_folder(folder):
    items = os.listdir(os.path.join(project_folder, folder))
    file_names = []
    for item in items:
        if "." in item:
            file_names.append(item)

    return file_names


def remove_and_rename_files(main_folder):
    main_path = os.listdir(os.path.join(project_folder, main_folder))
    print(main_path)
    folders = get_folders_from_folder(main_folder)

    for folder in folders:
        folder_path = os.path.join(main_folder, folder)
        files = get_files_from_folder(os.path.join(main_folder, folder))

        for file in files:
            file_index = files.index(file) + 1
            file_path = os.path.join(folder_path, file)
            file_name, file_ext = os.path.splitext(file_path)
            new_name = "{}_{}{}".format(folder, file_index, file_ext)
            new_path = os.path.join(main_folder, new_name)
            os.rename(file_path, new_path)

        os.rmdir(folder_path)


remove_and_rename_files(os.path.join(project_folder,"test_xlsxs"))
