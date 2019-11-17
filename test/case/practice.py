import os
from utils.config import DATA_FILE
path_list = []
version = 'pico'
version_upload_file = os.path.join(DATA_FILE, ''.join([version, '_upload']))
files_path = os.listdir(version_upload_file)
for file in files_path:
    if '4.5' in file:
        file_path = "\\".join([version_upload_file, file])
        print(file_path)
        print(os.listdir(file_path))
        for file_1 in os.listdir(file_path):
            path_list.append("\\".join([file_path, file_1]))
print(path_list)

for file in path_list:
    if file.endswith('.csv'):
        print(file)

