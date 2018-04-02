from Crawl import Crawl
import SubCrawl
from flask import Flask, request, render_template
import json
import re
import err
import DB

def do(path=[]) :
    db = DB.DB()
    siteName = request.args.get("name", "")
    url = request.args.get("url", "")
    if not re.match(r"https?://", url):
        return err.err("Url should be start with 'http://' or 'https://'")
    print("크롤링을 진행합니다.")
    crawled = appCrawl(url)
    print("크롤링을 완료했습니다.")
    print("\n\n\n\n")
    for line in crawled :
        db.insert(siteName, line)
    db.save()
    res = {
        "status" : "success",
        "code" : db.table2key(siteName)
    }
    return json.dumps(res)

def appCrawl(url) :
    crawl = Crawl(url)
    crawl.filter()
    crawled = []
    crawled.extend(crawl.get())
    crawled.extend(SubCrawl.deepCrawl(crawled))
    crawled = SubCrawl.deleteOverlap(crawled)
    crawled = SubCrawl.replaceAttack(crawled)
    crawled = SubCrawl.getAttackable(crawled)
    return crawled
