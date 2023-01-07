from .memory import LogicMemory
from .scaler import RewardScaler

# 負責記錄整個環境
class Environment:
    def __init__(self):
        self._memory = None
        self._scaler = None

    def SetMemory(self, memory: LogicMemory):
        self._memory = memory

    def SetScaler(self, scaler: RewardScaler):
        self._scaler = scaler

    def Step(self, trace, action=None):
        reward = 0
        if trace._opCode == 2:
            (hotDuplicateOffset, coldDuplicateOffset) = self._memory.WriteTrace(trace, action)
            reward += self._scaler.WriteOnHot(hotDuplicateOffset)
            reward += self._scaler.WriteOnCold(coldDuplicateOffset)
        print(reward)
        #elif trace._opCode == 1:
            #self.memory.ReadTrace(trace)
        