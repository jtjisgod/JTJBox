import os
import json
import hashlib

class DB :
    dbPath = "./database/"
    memory = {}
    def __init__(self) :
        if not os.path.isfile("schema.json") :
            json.dump({},open("schema.json", "w"))
        self.schema = json.load(open("schema.json"))
        removedTable = []
        for k, v in self.schema.items() :
            if not os.path.isfile(self.dbPath + v + ".json") :
                removedTable.append(k)
                continue
            self.memory[v] = json.load(open(self.dbPath + v + ".json"))
        for k in removedTable :
            del self.schema[k]
    def save(self) :
        json.dump(self.schema, open("schema.json", "w"))
        for k, v in self.memory.items() :
            json.dump(v, open(self.dbPath + k + ".json", "w"))
    def createTable(self, table) :
        if table not in self.schema.keys() :
            print("Table Created!")
            self.schema[table] = hashlib.sha512(table.encode()).hexdigest()
            self.memory[self.schema[table]] = []
    def insert(self, table, data) :
        self.createTable(table)
        self.memory[self.schema[table]].append(data)
        # self.memory[self.schema[table]] = self.memory.get(self.schema[table], []).append(data)
    def delete(self, table, data) :
        pass
    def select(self, table, data={}) :
        count = len(data.keys())
        res = []
        for i in range(0, len(self.memory.get(self.schema[table],[]))) :
            print(self.memory[self.schema[table]][i])
            flag = 0
            for tKey in self.memory[self.schema[table]][i].keys() :
                for key in data.keys() :
                    if key == tKey and data[key] == self.memory[self.schema[table]][i][key] :
                        flag += 1
            if flag == count :
                res.append(self.memory[self.schema[table]][i])
        return res
    def update(self, table, data) :
        pass
    def delRedup(self, table) :
        self.memory[self.schema[table]] = list(set(self.memory[self.schema[table]]))
    def table2key(self, table) :
        return self.schema.get(table, "")
    def key2table(self, key) :
        print(self.schema)
        for k, v in self.schema.items() :
            if v == key :
                return k
        return None
