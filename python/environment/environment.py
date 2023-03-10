from .reward import DynamicFixReward
from .memory import LogicMemory
from .reward import RewardScaler
from .state import StateLoader
from dotenv import load_dotenv
import random
import os
load_dotenv()
TRACE_FILE_PATH = os.getenv('TRACE_FILE_PATH')
TRACE_LOAD_LENGTH = int(os.getenv('TRACE_LOAD_LENGTH'))

class ActionSpace:
    def __init__(self):
        self._space = [True, False]
    
    def Sample(self):
        return random.choice(self._space)

# 負責記錄整個環境
class Environment:
    def __init__(self):
        self._memory = LogicMemory()
        self._scaler = RewardScaler()
        self._dynamicReward = DynamicFixReward()
        self._actionSpace = ActionSpace()
        self._stateLoader = StateLoader()
        self._stateLoader.Load(TRACE_FILE_PATH, TRACE_LOAD_LENGTH)
        self._tempState = None
        
    # 清除所有資訊到最一開始的樣子
    def ResetAll(self) -> None:
        self._tempState = None
        self._memory.ResetAll()
        self._stateLoader.ResetAll()
        self._dynamicReward.ResetAll()

    # 回歸到新的Episode並清除memory狀態, return 第一個state
    def ResetEpisode(self) -> None:
        self._memory.ResetAll()
        self._stateLoader.ResetEpisode()
        self._dynamicReward.ResetAll()
        self._tempState = self._stateLoader.GetState()
        return self._stateLoader.Preprocess(self._tempState)

    # 計算hot cold block ratio
    def GetHotColdBlockRatio(self) -> tuple:
        (hot, cold) = self._memory.GetHotColdBlockNums()
        total = hot + cold
        hotRatio = 0.0
        coldRatio = 0.0
        if total != 0:
            hotRatio = hot / total 
            coldRatio = cold / total 
        return (hotRatio, coldRatio)

    # 計算hot cold bytes ratio
    def GetHotColdBytesRatio(self) -> tuple:
        (hot, cold) = self._memory.GetHotColdBytes()
        total = hot + cold
        hotRatio = 0.0
        coldRatio = 0.0
        if total != 0:
            hotRatio = hot / total 
            coldRatio = cold / total 
        return (hotRatio, coldRatio)

    # 回傳reward, nextState
    def Step(self, action):
        dynamicReward = self._dynamicReward.Step(self._tempState.trace, action)
        (hotDuplicateOffset, coldDuplicateOffset) = self._memory.WriteTrace(self._tempState.trace, action)
        reward = self._scaler.GetWriteReward(hotDuplicateOffset, coldDuplicateOffset)
        reward += dynamicReward
        self._tempState = self._stateLoader.GetState()
        return reward, self._stateLoader.Preprocess(self._tempState)

