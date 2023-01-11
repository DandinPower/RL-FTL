from .memory import LogicMemory
from .scaler import RewardScaler

# 負責記錄整個環境
class Environment:
    def __init__(self):
        self._memory = None
        self._scaler = None
        
    # 回傳reward
    def Step(self, trace, action=None):
        if trace.IsWrite():
            (hotDuplicateOffset, coldDuplicateOffset) = self._memory.WriteTrace(trace, action)
            return self._scaler.GetWriteReward(hotDuplicateOffset, coldDuplicateOffset)
        elif trace.IsRead():
            (hotDuplicateOffset, coldDuplicateOffset) = self._memory.ReadTrace(trace)
            return self._scaler.GetReadReward(hotDuplicateOffset, coldDuplicateOffset)