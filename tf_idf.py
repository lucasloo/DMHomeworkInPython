import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from file_manager import FileWriter, FileReader


class TFIDF:
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.transformer = TfidfTransformer()

    def tf_idf(self, file_path):
        file_list = FileReader.get_file_list(file_path)
        corpus = []
        for file in file_list:
            file_reader = FileReader(file_path, file)
            try:
                content = file_reader.file_obj.read()
                corpus.append(content)
            finally:
                file_reader.close()
        tfidf = self.transformer.fit_transform(self.vectorizer.fit_transform(corpus))
        words = self.vectorizer.get_feature_names()
        weights = tfidf.toarray()
        output_path = 'tfidf_result/' + file_path + '/'
        for i in range(len(weights)):
            file_writer = FileWriter(output_path, str(i) + '.txt')
            try:
                for j in range(len(words)):
                    if weights[i][j] != 0:
                        file_writer.file_obj.write(words[j] + '\t' + str(weights[i][j]) + '\n')
            finally:
                file_writer.close()

    def tf_idf_sohu(self):
        file_path = 'result/sohu'
        dirs_list = FileReader.get_dirs(file_path)
        for tmp_dir in dirs_list:
            print("start " + tmp_dir + "\n")
            tfidf.tf_idf(file_path + "/" + tmp_dir + "/")
            print("finish " + tmp_dir + "\n")

    def test(self):
        file_path = 'result/sohu/财经/'
        tfidf.tf_idf(file_path)

tfidf = TFIDF()
tfidf.tf_idf_sohu()
# tfidf.test()

