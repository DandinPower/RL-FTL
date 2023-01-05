# 負責模擬現在的lba使用情況
class LogicBit:
    def __init__(self, address: int, type: bool):
        self._address = address
        self._type = type  
        
class LogicMemory:
    def __init__(self):
        self.bits = dict()  # list of LogicBits
    
    # 將一筆trace寫進memory
    def WriteTrace(self, trace, type):
        for i in range(trace._bytes):
            tempAddress = trace._lba + i
            self.bits[tempAddress] = type
            
    # 照lba address的順序來排
    def Sort(self):
        self.bits = sorted(self.bits)