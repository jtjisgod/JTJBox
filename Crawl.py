import urllib.request
import urllib.parse
import json
from bs4 import BeautifulSoup

class Crawl :
    rootUrl = ""
    crawled = []

    def getHTML(self, method, url, argParamData = "", argHeaders = None) :
        headers = { "User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0" }
        paramData = ""

        if argHeaders != None : headers.update(argHeaders)
        if argParamData != "" : paramData = urllib.parse.urlencode(argParamData)
        if method == "POST" : paramData = paramData.encode("utf-8")
        else :
            url += "?" + paramData
            paramData = None

        try :
            req = urllib.request.Request(url, data=paramData, headers=headers)
            read = urllib.request.urlopen(req).read()
            try : read = read.decode("utf-8")
            except : read
        except :
            read = ""

        return read



    # Url parsing and checking is vailid Url
    # Author : JTJ
    # Last fix : 2016.09.14. 23:04
    def checkAndGet(self, tag, url = None) :
        # if url == None : url = target.getUrl()
        url = tag.get("href")
        if url == None : url = tag.get("src")
        if url == None : url = tag.get("link")
        if url == None : url = tag.get("action")
        if url != None and url != '#' :
            if url.count("?") > 1   : return False
            if url.find('#') != -1  : return False
            if url.find('.js') != -1: return False
            if url[0:7] == "mailto:": return False
            if url[0:4] == "tel:"   : return False
            if url[0:2] == "./"     : url = url.replace("./", "")
            if url[0:2] == "//"     : url = "http:" + url
            if url[0:4] != "http" and url[0:3] != "ftp" and url[0:2] != "//" :
                if url[0] == "/" : url = self.rootUrl + url
                else : url = self.rootUrl + "/" + url
            #     s = url.split("/")
            #     if url == target.getUrl() : url = url + "/" + url
            #     else : url = "/".join(s[0:len(s)-1]) + "/" + url
            # if url.find(target.getUrl().split("//")[1].split("/")[0]) == -1 : return False
            # if url.count("//") > 1 : return False
            return url

    def parseForm(self, tag)  :
        action = tag.attrs["action"]
        if action[0:2] == "./"     : action = action.replace("./", "")
        if action[0:2] == "//"     : action = "http:" + action
        if action[0:4] != "http" and action[0:3] != "ftp" and action[0:2] != "//" :
            if action[0] == "/" : action = self.rootUrl + action
            else : action = self.rootUrl + "/" + action
        inputs = self.getInput(tag)
        param = []
        for ipt in inputs :
            param.append(ipt.attrs["name"])
        ret = {
            "method" : "POST",
            "url" : action,
            "param" : param
        }
        return ret

    def getInput(self, inputTag) :
        output = []
        tags = inputTag.find_all()
        for tag in tags :
            if tag.name == "input" :
                output.append(tag)
            elif len(tag.find_all()) == 0 :
                return []
            else :
                pppp = self.getInput(tag)
                output.extend(pppp)
                return output
        return output

    def __init__(self, url) :

        protocol = url.split("//")[0]

        try : domain = url.split("//")[1].split("/")[0]
        except : domain = url.split("//")[1]

        url = protocol + "//" + domain

        if url[-1] == "/" :
            url = url[0:-1]
        self.rootUrl = url
        param = {  }

        html = self.getHTML("GET", self.rootUrl)
        soup = BeautifulSoup(html, "lxml")
        tags = soup.find_all()
        for tag in tags :
            if tag.name == "form" :
                self.crawled.append(self.parseForm(tag))
            else :
                try :
                    url = self.checkAndGet(tag)
                    if url == False or url == None : continue
                    payload = {
                        "method" : "GET",
                        "url"  : url
                    }
                    try: self.crawled.index(payload)
                    except: self.crawled.append(payload)
                except :
                    pass

        for i in range(0, len(self.crawled)) :
            if self.crawled[i]['url'][0] == "/" :
                self.crawled[i]['url'] = self.rootUrl + self.crawled[i]['url']

    def filter(self) :
        crawled = []
        for i in range(0, len(self.crawled)) :
            # print(self.rootUrl + "   " + self.crawled[i]['url'][0:len(self.rootUrl)])
            try :
                domain = self.crawled[i]['url'].split("//")[1].split("/")[0]
                rootUrl = self.rootUrl.split("//")[1]
                # print(rootUrl + "   " + domain)
                if rootUrl == domain :
                    crawled.append(self.crawled.pop(i))
            except :
                pass
        self.crawled = crawled

    def get(self) :
        # print(self.crawled)
        return self.crawled

if __name__ == '__main__':
    crawl = Crawl("https://ecampus.kookmin.ac.kr/login.php")
    crawled = crawl.get()
    for i in crawled :
        print(i)
