from ..environment.trace_loader import TraceLoader
from ..environment.environment import Environment
from ..environment.memory import LogicMemory
from ..environment.scaler import RewardScaler
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import numpy as np

from dotenv import load_dotenv
from tqdm import tqdm
import random
import os
load_dotenv()
TRACE_FILE_PATH = os.getenv('TRACE_FILE_PATH')
TRACE_LOAD_LENGTH = int(os.getenv('TRACE_LOAD_LENGTH'))

class Agent:
    def __init__(self):
        self._environment = Environment()
        self._memory = LogicMemory()
        self._traceLoader = TraceLoader()
        self._scaler = RewardScaler()
        self._scaler2 = StandardScaler()
        self.Initialize()
        
    def Initialize(self):
        self._environment.SetMemory(self._memory)
        self._environment.SetScaler(self._scaler)
        self._traceLoader.Load(TRACE_FILE_PATH, TRACE_LOAD_LENGTH)
        self._scaler.Fit(self._traceLoader.GetAddresses())

    def Train(self):
        for i in tqdm(range(TRACE_LOAD_LENGTH)):
            tempTrace = self._traceLoader.GetTrace()
            if tempTrace.IsRead():
                self._environment.Step(tempTrace)
            elif tempTrace.IsWrite():
                self._environment.Step(tempTrace, self.GetAction(tempTrace))

    # 測試功能
    def Test(self):
        duplicateList = np.array(list(self._environment._duplicateRecord))
        duplicateList = duplicateList.reshape(-1,1)
        self._scaler2.fit(duplicateList)
        print(duplicateList)
        result = self._scaler2.transform(duplicateList)
        a = self._scaler2.transform([[7913472]])[0][0]
        b = (a - result.min()) / (result.max() - result.min())
        b = b * (10) + 0
        print(b)
    
    # True為Hot, False為Cold
    def GetAction(self, trace):
        return random.choice([True, False])

    def ShowMemoryAfterSort(self):
        self._memory.Sort()
        print(self._memory)