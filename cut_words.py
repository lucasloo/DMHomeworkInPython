import jieba
from file_manager import FileWriter, FileReader


class CutWords:
    @staticmethod
    def cut_words(file_path, file_name):
        file_reader = FileReader(file_path, file_name)
        try:
            contents = file_reader.file_obj.read()
            seg_list = jieba.cut(contents, cut_all=True)
            result = []
            for seg in seg_list:
                if seg != '' and seg != '\n':
                    result.append(seg)
        finally:
            file_reader.close()
        return result

    @staticmethod
    def cut_sohu_words():
        file_path = 'sohu/'
        result_path = 'result/'
        dirs_list = FileReader.get_dirs(file_path)
        for tmp_dir in dirs_list:
            files_list = FileReader.get_file_list(file_path + tmp_dir)
            for tmp_file in files_list:
                result = CutWords.cut_words(file_path + tmp_dir + '/', tmp_file)
                file_writer = FileWriter(result_path + file_path + tmp_dir + '/', tmp_file)
                try:
                    file_writer.file_obj.write(' '.join(result))
                finally:
                    file_writer.close()
            print('finish' + tmp_dir + '\n')

CutWords.cut_sohu_words()
