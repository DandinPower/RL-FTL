from collections import namedtuple
from .trace_loader import TraceLoader
from .memory import LogicMemory
from .scaler import RewardScaler
from dotenv import load_dotenv
import random
import os
load_dotenv()
TRACE_FILE_PATH = os.getenv('TRACE_FILE_PATH')
TRACE_LOAD_LENGTH = int(os.getenv('TRACE_LOAD_LENGTH'))

class FidTokenizer:
    def __init__(self):
        self.datas = dict()
    
    def ResetAll(self):
        self.datas.clear()

    def __getitem__(self, key):
        if self.datas.get(key) == None:
            self.datas[key] = len(self.datas)
        return self.datas[key]

State = namedtuple('State', ['trace', 'fid_token', 'lba_difference', 'num_bytes'])
class StateLoader:
    def __init__(self) -> None:
        self._traceLoader = TraceLoader()
        self._tokenizer = FidTokenizer()
        self._lastTrace = None 

    def ResetAll(self):
        self._traceLoader.ResetAll()
        self._tokenizer.ResetAll()
        self._lastTrace = None 

    def ResetEpisode(self):
        self._tokenizer.ResetAll()
        self._lastTrace = None

    def Load(self, path, length = -1):
        self._traceLoader.Load(path, length)

    def CountTraceDifference(self, trace):
        if self._lastTrace:
            return trace._lba - self._lastTrace._lba
        else:
            return 0

    def GetState(self):
        trace = self._traceLoader.GetWriteTrace()
        fid_token = self._tokenizer[trace._fid]
        lba_difference = self.CountTraceDifference(trace)
        state = State(trace=trace, fid_token=fid_token, lba_difference=lba_difference, num_bytes=trace._bytes)
        self._lastTrace = trace
        return state

# 負責記錄整個環境
class Environment:
    def __init__(self):
        self._memory = LogicMemory()
        self._scaler = RewardScaler()
        self._stateLoader = StateLoader()
        self._stateLoader.Load(TRACE_FILE_PATH, TRACE_LOAD_LENGTH)
        self._sampleSpace = [True, False]
        self._tempState = None
        
    # 清除所有資訊到最一開始的樣子
    def ResetAll(self) -> None:
        self._tempState = None
        self._memory.ResetAll()
        self._stateLoader.ResetAll()

    # 回歸到新的Episode並清除memory狀態, return 第一個state
    def ResetEpisode(self) -> None:
        self._memory.ResetAll()
        self._stateLoader.ResetEpisode()
        self._tempState = self._stateLoader.GetState()
        return self._tempState

    # 回傳reward, nextState
    def Step(self, action):
        (hotDuplicateOffset, coldDuplicateOffset) = self._memory.WriteTrace(self._tempState.trace, action)
        reward = self._scaler.GetWriteReward(hotDuplicateOffset, coldDuplicateOffset)
        self._tempState = self._stateLoader.GetState()
        return reward, self._tempState

