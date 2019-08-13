import sys
import os
import hashlib
from collections import Counter
import copy


def path_validator(directory_name):
    if os.path.exists(directory_name):
        print("Path validation: {}".format(directory_name))
        return True
    return False


def get_file_hash(file_path):
    h = hashlib.md5()
    with open(file_path, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)

    return h.hexdigest()


def get_files_data(directory):
    files_dict = {}
    for root, dir, files in os.walk(directory):
        for file_item in files:
            file_path = os.path.join(root, file_item)
            file_hash = get_file_hash(file_path)
            file_data = {
                file_path: file_hash
            }
            files_dict.update(file_data)
    return files_dict


def delete_file_duplicates(files_data):
    hashes = [hash for name, hash in files_data.items()]
    hashes_count = Counter(hashes)
    deleted_files = []
    for hash in hashes:
        value_count = hashes_count.get(hash)
        occurences_to_remove = value_count - 1
        files_dict = copy.deepcopy(files_data)
        for key, value in files_dict.items():
            if hash == value and occurences_to_remove:
                os.remove(key)
                deleted_files.append(key)
                del files_data[key]
                occurences_to_remove -= 1
            else:
                break
    return deleted_files


if __name__ == '__main__':
    print("=====Start Looking for Duplicate Files=====")
    directory_path = None
    try:
        directory_path = sys.argv[1]
    except IndexError as error:
        print("Error! Please include a file path")

    if directory_path:
        files_dict = get_files_data(directory_path)
        if files_dict:
            deleted_files = delete_file_duplicates(files_dict)
            for deleted_file in deleted_files:
                print("File successfully deleted: ", deleted_file)
            if not deleted_files:
                print("No duplicates found. No files were deleted")
        else:
             print("No files found.")
    print("=====Finished Processing Script=====")




