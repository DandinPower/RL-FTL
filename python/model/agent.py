from ..environment.trace_loader import TraceLoader
from ..environment.environment import Environment
from ..environment.memory import LogicMemory
from ..environment.scaler import RewardScaler
from ..libs.history import History
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
        self._history = History()
        self.Initialize()
        
    def Initialize(self):
        self._environment._memory = self._memory
        self._environment._scaler = self._scaler
        self._traceLoader.Load(TRACE_FILE_PATH, TRACE_LOAD_LENGTH)

    def Train(self):
        for i in tqdm(range(TRACE_LOAD_LENGTH)):
            tempTrace = self._traceLoader.GetTrace()
            reward = 0
            if tempTrace.IsRead():
                reward = self._environment.Step(tempTrace)
                self._history.Add(tempTrace, None, reward)
            elif tempTrace.IsWrite():
                action = self.GetAction(tempTrace)
                reward = self._environment.Step(tempTrace, action)
                self._history.Add(tempTrace, action, reward)
        self._history.WriteHistory('python/history/record.csv')

    # True為Hot, False為Cold
    def GetAction(self, trace):
        return random.choice([True, False])