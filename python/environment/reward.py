from ..libs.statistic import Entries
from collections import deque
from dotenv import load_dotenv
import numpy as np
import os
load_dotenv()

WRITE_ON_HOT_MAX = int(os.getenv('WRITE_ON_HOT_MAX'))
WRITE_ON_HOT_MIN = int(os.getenv('WRITE_ON_HOT_MIN'))
WRITE_ON_COLD_MAX = int(os.getenv('WRITE_ON_COLD_MAX'))
WRITE_ON_COLD_MIN = int(os.getenv('WRITE_ON_COLD_MIN'))
READ_ON_HOT_MAX = int(os.getenv('READ_ON_HOT_MAX'))
READ_ON_HOT_MIN = int(os.getenv('READ_ON_HOT_MIN'))
READ_ON_COLD_MAX = int(os.getenv('READ_ON_COLD_MAX'))
READ_ON_COLD_MIN = int(os.getenv('READ_ON_COLD_MIN'))

NOT_ACCESS_IS_COLD = int(os.getenv('NOT_ACCESS_IS_COLD'))
NOT_ACCESS_IS_HOT = int(os.getenv('NOT_ACCESS_IS_HOT'))

class RewardScaler:
    def __init__(self):
        pass

    # 根據hot cold 比例來給予reward
    def GetWriteReward(self, hotDuplicateOffset: int, coldDuplicateOffset: int) -> int:
        total = hotDuplicateOffset + coldDuplicateOffset
        if total == 0:
            return 0
        else:
            hotRate = hotDuplicateOffset / total 
            coldRate = coldDuplicateOffset / total 
            return self.GetRewardFromRate(hotRate, WRITE_ON_HOT_MIN, WRITE_ON_HOT_MAX) + self.GetRewardFromRate(coldRate, WRITE_ON_COLD_MIN, WRITE_ON_COLD_MAX)

    # 根據hot cold 比例來給予reward
    def GetReadReward(self, hotDuplicateOffset: int, coldDuplicateOffset: int) -> int:
        total = hotDuplicateOffset + coldDuplicateOffset
        if total == 0:
            return 0
        else:
            hotRate = hotDuplicateOffset / total 
            coldRate = coldDuplicateOffset / total 
            return self.GetRewardFromRate(hotRate, READ_ON_HOT_MIN, READ_ON_HOT_MAX) + self.GetRewardFromRate(coldRate, READ_ON_COLD_MIN, READ_ON_COLD_MAX)        

    def GetRewardFromRate(self, rate: float, minOfRange: int, maxOfRange: int) -> int:
        return (rate * (maxOfRange - minOfRange)) + minOfRange

class FixRewardQueue:
    def __init__(self) -> None:
        self.queue = deque()
    
    def ResetAll(self):
        self.queue.clear()

    # type為true代表沒被access到且為hot
    def AddNewReward(self, type):
        if type:
            self.queue.append(NOT_ACCESS_IS_HOT)
        else:
            self.queue.append(NOT_ACCESS_IS_COLD)

    def GetReward(self):
        return self.queue.pop()

    def __len__(self):
        return len(self.queue)

class DynamicFixReward:
    def __init__(self) -> None:
        self._entries = Entries()
        self._fixReward = FixRewardQueue()

    def ResetAll(self):
        self._entries.ResetAll()
        self._fixReward.ResetAll()
    
    def Step(self, trace, action) -> int:
        self._entries.Add(trace._fid, trace._lba, trace._bytes, action)
        if len(self._fixReward) > 0:
            return self._fixReward.GetReward()
        reward = 0
        if self._entries.GetFinishLength() > 0:
            finishEntries = self._entries.GetFinishEntriesAndClear()
            for entry in finishEntries:
                if entry._type == False:
                    self._fixReward.AddNewReward(entry._action)
        if len(self._fixReward) > 0:
            reward = self._fixReward.GetReward()
        return reward