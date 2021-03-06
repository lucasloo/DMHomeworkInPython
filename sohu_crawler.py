import urllib
import sys
from bs4 import BeautifulSoup
from urllib import request, error
from file_manager import FileWriter


class SohuCrawler:
    def __init__(self):
        self.index_list = []
        self.page = None
        self.type = ''
        self.file_writer = None
        self.total = 0

    def init_index_list(self, index):
        counter = 1
        while counter < 1500:
            print("initializing list " + str(counter) + '...')
            url = SohuCrawler.get_list_url(index, counter)
            if self.init_page(url):
                soup = BeautifulSoup(self.page, "html.parser")
                # init the type
                if self.type == '' and soup.find(class_="cTtl"):
                    self.type = soup.find(class_="cTtl").string
                # init the index_list
                for content in soup.find_all('a', class_="h4 h4New"):
                    self.index_list.append(content.get("href"))
            counter += 1

    def crawler(self):
        for tmp in self.index_list:
            tmp_url = "http://m.sohu.com" + tmp
            if self.init_page(tmp_url):
                soup = BeautifulSoup(self.page, "html.parser")
                # init file writer
                self.file_writer = FileWriter('sohu/' + self.type + '/', str(self.total) + '.txt')
                try:
                    # get title
                    if soup.find('h1', class_='h1') and soup.find('h1', class_='h1').string:
                        title = soup.find('h1', class_='h1').string
                        self.file_writer.file_obj.write(title + '\n')
                    # get content
                    contents = soup.find_all('p', class_='para')
                    for content in contents:
                        if content.string:
                            self.file_writer.file_obj.write(content.string + '\n')
                finally:
                    self.file_writer.close()
            self.total += 1
            print("current:" + str(self.total))

    def init_page(self, url):
        try:
            url_request = urllib.request.Request(url)
            response = urllib.request.urlopen(url_request)
            self.page = response.read().decode(sys.getfilesystemencoding())
            return True
        except error.URLError:
            self.page = None
            print("url error\n")
            return False
        except ConnectionResetError:
            print("ConnectionResetError\n")
            return False
        except UnicodeDecodeError:
            print('UnicodeDecodeError')
            return False

    @staticmethod
    def get_list_url(index, num):
        return "http://m.sohu.com/cr/" + str(index) + "/?page=" + str(num)

    def clear(self):
        self.file_writer = None
        self.index_list.clear()
        self.page = None
        self.type = ''
        self.total = 0

    def start(self):
        index = 18
        while index < 22:
            self.init_index_list(index)
            self.crawler()
            print("finish crawling:" + self.type)
            self.clear()
            index += 1

crawler = SohuCrawler()
crawler.start()
