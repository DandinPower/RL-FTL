from collections import deque
import random

class ReplayBuffer:
    #初始化
    def __init__(self, _maxlen):
        self.memory = deque(maxlen= _maxlen)
    
    #儲存一個step的資訊
    def Add(self, _st, _at, _rt, _st1):
        temp = (_st, _at, _rt, _st1)
        self.memory.append(temp)

    #取得batch資料
    def GetBatchData(self, _batchSize):
        data = random.sample(self.memory, _batchSize)
        return data
    
    #取得目前長度
    def __len__(self):
        return len(self.memory)

    def __getitem__(self, index):
        return self.memory[index]