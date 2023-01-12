class FidTokenizer:
    def __init__(self):
        self.datas = dict()
    
    def ResetAll(self):
        self.datas.clear()

    def __getitem__(self, key):
        if self.datas.get(key) == None:
            self.datas[key] = len(self.datas)
        return self.datas[key]