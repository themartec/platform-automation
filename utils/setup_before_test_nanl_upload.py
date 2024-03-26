import csv
import os
import shutil


def remove_folder(dir_to_remove):
    shutil.rmtree(dir_to_remove)


def remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        print(f"The file {file_name} is removed")
    else:
        print("The file does not exist")


def init_csv_file_with_column(column_name, filename):
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(column_name)


