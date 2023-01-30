from collections import namedtuple

FidTokenData = namedtuple('FidTokenData', ['id', 'count'])

class FidTokenizer:
    def __init__(self):
        self.datas = dict()
    
    def __getitem__(self, key):
        temp = self.datas.get(key)
        if  temp == None:
            self.datas[key] = FidTokenData(id = len(self.datas), count = 0)
        else:
            self.datas[key] = temp._replace(count = temp.count + 1)
        return self.datas[key].id

    def ResetAll(self):
        self.datas.clear()