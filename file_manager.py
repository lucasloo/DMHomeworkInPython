import os


class FileWriter:
    def __init__(self, file_path, file_name):
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        self.file_obj = open(file_path + file_name, 'w')

    def close(self):
        self.file_obj.close()


class FileReader:
    def __init__(self, file_path, file_name):
        self.file_obj = open(file_path + file_name, 'r+')

    @staticmethod
    def get_file_list(file_path):
        file_list = []
        files = os.listdir(file_path)
        for file in files:
            if file[0] == '.':
                continue
            else:
                file_list.append(file)
        return file_list

    def close(self):
        self.file_obj.close()
