import sys
import flask
from flask import Flask, request, render_template

import re
import configparser
from urllib.parse import urlparse

import DB

import UpdateCrawling
import UpdateDetail
import UpdateSend

updateFunc = {
    "crawling" : UpdateCrawling,
    "detail" : UpdateDetail,
    "send" : UpdateSend
}

config = configparser.RawConfigParser()
config.read('config.properties')

app = Flask(__name__)

@app.route('/', defaults={'path': '/'})
@app.route('/<path:path>', methods=["POST", "GET"])
def catch_all(path):

    path = path.split("/")

    page = {
        "template" : "search.html"
    }

    if path[0] == "update" :
        return update(path)
    elif path[0] == "detail" :
        db = DB.DB()
        page['template'] = "detail.html"
        if re.match('^[\w-]+$', path[1]) :
            page['code'] = path[1]
        else :
            return "<script> location.href='/'; </script>"
        page['title'] = db.key2table(page['code'])
    elif path[0] == "send" :

        db = DB.DB()
        page['template'] = "send.html"
        if re.match('^[\w-]+$', path[1]) :
            page['code'] = path[1]
        else :
            return "<script> location.href='/'; </script>"
        try :
            int(path[2])
        except :
            return "<script> location.href='/'; </script>"
        selected = db.select(db.key2table(page['code']))
        getParam = []
        url = selected[int(path[2])]['url']
        if "?" in url :
            for p in url.split("?")[1].split("&") :
                getParam.append(p.split("=")[0])
        header = {}
        for key in config.items("Request") :
            key = list(key)
            if not key[1] :
                if key[0] == "header.host" :
                    key[1] = urlparse(url).netloc
                elif key[0] == "header.referer" :
                    key[1] = url.replace("{{payload}}", "")
            header[key[0]] = key[1]
        page['header'] = header
        page['target'] = selected[int(path[2])]
        page['title'] = db.key2table(page['code'])
        page['getParam'] = getParam
    
    db = DB.DB()
    page['pages'] = db.schema

    return render_template("index.html", page=page)

def update(path) :
    return updateFunc.get(path[1], NotFound).do(path)

class NotFound :
    def do(self) :
        return "Not Found"

def main()  :
    app.debug = True
    app.run(host='0.0.0.0')

if __name__ == '__main__' :
    main()
