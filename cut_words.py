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
        file_writer = FileWriter("result/", file_name)
        file_writer.file_obj.write(' '.join(result))
        file_writer.close()

    @staticmethod
    def cut_sohu_words():
        file_path = 'sohu/'
        file_list = FileReader.get_file_list(file_path)
        for file_name in file_list:
            CutWords.cut_words(file_path, file_name)

CutWords.cut_sohu_words()
