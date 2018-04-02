import json

def err(string) :
    return json.dumps({
        "status": "err",
        "message": string
    })