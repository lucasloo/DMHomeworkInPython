import os


class FileWriter:
    def __init__(self, file_path, file_name):
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        self.file_obj = open(file_path + file_name, 'w')
