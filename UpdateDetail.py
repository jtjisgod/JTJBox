from flask import Flask, request, render_template
import json
import err
import DB

def do(path=[]) :
    if len(path) != 3 :
        return err.err("Error")
    db = DB.DB()
    table = db.key2table(path[2])
    if table == None :
        return err.err("Error Data is not exist.\n" + path[2])
    res = {
        "status" : "success",
        "result" : db.select(table)
    }
    return json.dumps(res)