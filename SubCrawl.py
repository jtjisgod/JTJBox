from Crawl import Crawl

def deepCrawl(crawled) :
    tmp = []
    for each in crawled :
        crawl = Crawl(each['url'])
        crawl.filter()
        tmp.extend(crawl.get())
    return tmp

def deleteOverlap(crawled) :
    for i in range(0, len(crawled)) :
        for j in range(0, len(crawled)) :
            if i != j and crawled[i] == crawled[j] :
                crawled[j] = None
    output = []
    for i in range(0, len(crawled)) :
        if crawled[i] != None :
            output.append(crawled[i])
    return output

def replaceAttack(crawled) :
    for i in range(0, len(crawled)) :

        url = crawled[i]['url']
        if ("?" in url) == False: continue

        left =  url.split("?")[0]
        right = url.split("?")[1]
        params = right.split("&")
        joined = ""
        for j in range(0, len(params)) :
            valueName = params[j].split("=")[0]
            joined += valueName + "=" + "{{payload}}" + "&"

        url = left + "?" + joined[0:-1]
        crawled[i]['url'] = url

    crawled = deleteOverlap(crawled)

    return crawled

def getAttackable(crawled) :

    output = []
    for each in crawled :
        if (each['method'] == "POST") :
            output.append(each)
        elif ("{{payload}}" in each['url']) == True :
            output.append(each)

    return output
