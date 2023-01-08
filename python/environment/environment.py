from .memory import LogicMemory
from .scaler import RewardScaler
from ..libs.history import History

# 負責記錄整個環境
class Environment:
    def __init__(self):
        self._memory = None
        self._scaler = None
        self._history = History()

    def SetMemory(self, memory: LogicMemory):
        self._memory = memory

    def SetScaler(self, scaler: RewardScaler):
        self._scaler = scaler

    # 回傳reward
    def Step(self, trace, action=None):
        reward = 0
        if trace._opCode == 2:
            (hotDuplicateOffset, coldDuplicateOffset) = self._memory.WriteTrace(trace, action)
            reward += self._scaler.WriteOnHot(hotDuplicateOffset)
            reward += self._scaler.WriteOnCold(coldDuplicateOffset)
            self._history.Step(hotDuplicateOffset)
            self._history.Step(coldDuplicateOffset)
        elif trace._opCode == 1:
            (hotDuplicateOffset, coldDuplicateOffset) = self._memory.ReadTrace(trace)
            reward += self._scaler.ReadOnHot(hotDuplicateOffset)
            reward += self._scaler.ReadOnCold(coldDuplicateOffset)
            self._history.Step(hotDuplicateOffset)
            self._history.Step(coldDuplicateOffset)
        return reward
    
    # 把self._history紀錄的數據寫進csv
    def WriteDuplicateHistory(self, path):
        self._history.Sort()
        self._history.Write(path)