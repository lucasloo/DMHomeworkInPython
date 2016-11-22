# -*- coding:utf-8 -*-
import urllib
import re
import  sys
from urllib import request,error
from Tool import *


class Crawler:

    def __init__(self, baseUrl, seeLZ):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz='+str(seeLZ)
        self.tool = Tool()
        self.page = None

    def getPage(self, page_num):
        try:
            url = self.baseURL + self.seeLZ + "&pn=" + str(page_num)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            the_page = response.read()
            coding_type = sys.getfilesystemencoding()
            # print(the_page.decode(coding_type))
            self.page = the_page.decode(coding_type)
        except urllib.error.URLError as e:
            print(e.reason)
            return None

    def getPageNum(self):
        # 获取帖子页数的正则表达式
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>', re.S)
        result = re.search(pattern, self.page)
        if result:
            return int(result.group(1).strip())
        else:
            return None

    def getTitle(self):
        self.getPage(1)
        pattern = re.compile('<h3 class="core_title_txt pull-left text-overflow.*?>(.*?)</h3>',re.S)
        result = re.search(pattern, self.page)
        if result:
            print(result.group(1))
        else:
            return None

    def getComment(self):
        pattern = re.compile('<div id="post_content_.*? class="d_post_content j_d_post_content ">(.*?)</div>', re.S)
        result = re.findall(pattern, self.page)
        for comment in result:
            print(self.tool.replace(comment))

    def start(self):
        self.getTitle()
        page_total_num = self.getPageNum()
        for i in range(1, page_total_num + 1):
            self.getPage(i)
            self.getComment()

baseURL = 'http://tieba.baidu.com/p/3138733512'
baiduCrawler = Crawler(baseURL, 1)
baiduCrawler.start()
