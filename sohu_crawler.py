import urllib
import sys
from bs4 import BeautifulSoup
from urllib import request, error
from file_writer import FileWriter


class SohuCrawler:
    def __init__(self):
        self.index_list = []
        self.page = None
        self.type = ''
        self.file_writer = None
        self.total = 0

    def init_index_list(self, index):
        counter = 1
        while counter < 10:
            print("initializing list " + str(counter) + '...')
            url = self.get_list_url(index, counter)
            if self.init_page(url):
                soup = BeautifulSoup(self.page, "html.parser")
                # init the type
                if self.type == '' and soup.find(class_="cTtl"):
                    self.type = soup.find(class_="cTtl").string
                # init file writer
                if self.file_writer is None:
                    self.file_writer = FileWriter('sohu/', self.type + '.txt')
                # init the index_list
                for content in soup.find_all('a', class_="h4 h4New"):
                    self.index_list.append(content.get("href"))
            counter += 1

    def crawler(self):
        try:
            for tmp in self.index_list:
                tmp_url = "http://m.sohu.com" + tmp
                if self.init_page(tmp_url):
                    soup = BeautifulSoup(self.page, "html.parser")
                    # get title
                    if soup.find('h1', class_='h1') and soup.find('h1', class_='h1').string:
                        title = soup.find('h1', class_='h1').string
                        self.file_writer.file_obj.write(title + '\n')
                    # get content
                    contents = soup.find_all('p', class_='para')
                    for content in contents:
                        if content.string:
                            self.file_writer.file_obj.write(content.string + '\n')
                self.total += 1
                print("current:" + str(self.total))
            self.file_writer.file_obj.write('\n')
        finally:
            self.file_writer.file_obj.close()

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
        except error.HTTPError:
            print("http error\n")
            return False
        except ConnectionResetError:
            print("ConnectionResetError\n")
            return False

    def get_list_url(self, index, num):
        return "http://m.sohu.com/cr/" + str(index) + "/?page=" + str(num)

    def clear(self):
        self.file_writer = None
        self.index_list.clear()
        self.page = None
        self.type = ''
        self.total = 0

    def start(self):
        index = 2
        while index < 20:
            self.init_index_list(index)
            self.crawler()
            print("finish crawling:" + self.type)
            self.clear()
            index += 1

crawler = SohuCrawler()
crawler.start()
