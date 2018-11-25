#coding= utf-8
import requests

class Tiebaspider:
    def __init__(self,tieba_name):
        self.tieba_name = tieba_name
        self.url_temp = "http://tieba.baidu.com/f?kw="+ tieba_name +"&ie=utf-8&pn={}"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
    def get_url_list(self):
        url_list = []
        for i in range (1000):
            url_list.append(self.url_temp.format(i*50))
        return url_list
    def parse_url(self,url):
        response = requests.get(url,headers = self.headers )
        return response.content.decode()

    def save_html(self,html,num):
        file_path = "{}-帝{}也.html".format(self.tieba_name,num)
        with open(file_path,"w",encoding="utf-8") as f:
            f.write(html)

    def run(self):
        url_list = self.get_url_list()
        for url in url_list:
            html = self.parse_url(url)
            num = url_list.index(url) + 1
            self.save_html(html,num)



if __name__ == "__main__":
    tieba_spider = Tiebaspider("李毅")
    tieba_spider.run()