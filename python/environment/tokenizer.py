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

class RangeTokenizer:
    def __init__(self, *args):
        self._sampleSize = args
    
    def GetToken(self, key):
        for index, threshold in enumerate(self._sampleSize):
            if key <= threshold:
                return index
        maxIndex = len(self._sampleSize)
        return maxIndex

    def __getitem__(self, key):
        key = abs(key)
        return self.GetToken(key)
    
class FrequencyTokenizer:
    def __init__(self, size, range):
        self._size = size
        self._range = range - 1
        self._datas = dict()
    
    def GetToken(self, key):
        freq = self._datas[key]
        temp = freq // self._size 
        if temp > self._range:
            temp = self._range 
        return temp
        
    def Add(self, key):
        if self._datas.get(key) == None:
            self._datas[key] = 0
        else:
            self._datas[key] = 1 + self._datas.get(key)

    def __getitem__(self, key):
        self.Add(key)
        return self.GetToken(key)


