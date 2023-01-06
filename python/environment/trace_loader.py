import pandas as pd
from ..libs.logs import PrintLog
from .trace import Trace
from tqdm import tqdm

class TraceLoader:
    def __init__(self):
        self._traces = []
        self._current = 0
    
    # 將trace csv load 進來
    def Load(self, path, length=-1):
        PrintLog('use pandas to read csv....')
        self._traces.clear()
        df = pd.read_csv(path, header = None, delimiter=',', lineterminator='\n')
        loadCount = 0
        totalCount = len(df.index)
        readCount = 0
        if length == -1: readCount = totalCount 
        else: readCount = length 
        for index, row in tqdm(df.iterrows(), total = readCount):
            loadCount += 1
            temp = Trace(row[0], row[1], row[2], row[3])
            self._traces.append(temp)
            if loadCount == length:
                break

    def Reset(self):
        self._current = 0

    def GetTrace(self):
        index = self._current 
        self._current += 1
        return self._traces[index]
    
    def GetLength(self):
        return len(self._traces)
    
    
    