class Load():
    defaultPath = "./payload/{{category}}/"
    defaultAttackRet = ""
    defaultPayload = ""
    category = ""
    def __init__(self, category, rep=""):
        self.category = category
        self.defaultPath = self.defaultPath.replace("{{category}}", category)
        self.defaultAttackRet = self.defaultPath + "attackRet"
        self.defaultPayload = self.defaultPath + "payload"
    def getAttackRet(self) :
        lines = self.load(self.defaultAttackRet).split("\n")
        arr = []
        for line in lines :
            if line != "" :
                cutted = line.split(",")
                arr.append((cutted[0].strip(), cutted[1].strip()))
        return arr
    def getRet(self) :
        lines = self.load(self.defaultPayload).split("\n")
        lines.pop()
        return lines
    def load(self,filename) :
        f = open(filename, 'r')
        read = f.read()
        f.close()
        return read
    def get(self) :
        return (self.getAttackRet(), self.getRet())

if __name__ == '__main__':
    LoadCml = Load("commandline")
    LoadXss = Load("xss")
    print(LoadCml.get())
    print(LoadXss.get())
