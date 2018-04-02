from flask import Flask, request, render_template
import json
import err
import DB
import urllib
import time

def do(path=[]) :

    req = json.loads(request.form.get("data", "\"false\""))

    if req == "false" :
        return err.err("Err")

    url = req['url'].split("?")[0] + "?"

    postData = {}
    for param in req['params'] :
        if param['method'].lower() == "get" :
            url += param['name'] + "=" + urllib.parse.quote_plus(param['value']) + "&"
        else :
            postData[param['name']] = param['value']

    headers = {}
    for header in req['headers'] :
        headers[header['key']] = header['value']

    startTime = time.time()
    req = urllib.request.Request(url, data=urllib.parse.urlencode(postData).encode(), headers=headers)
    read = urllib.request.urlopen(req).read()
    try : read = read.decode("utf-8")
    except : read

    ret = {
        "time": time.time() - startTime,
        "html": read
    }

    return json.dumps(ret)