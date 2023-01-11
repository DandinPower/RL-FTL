from sklearn.preprocessing import StandardScaler
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