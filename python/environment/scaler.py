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
        self._scaler = StandardScaler()
        self._max = 0
        self._min = 0

    # 將loading進來的x做標準化
    def Fit(self, x: list):
        x = np.array(x)
        x = x.reshape(-1, 1)
        self._scaler.fit(x)
        result = self._scaler.transform(x)
        self._max = result.max()
        self._min = result.min()
    
    # 根據覆蓋的範圍做標準化後映射到reward的範圍內回傳reward (應用在寫入到Hot資料時)
    def WriteOnHot(self, duplicateOffset: int) -> int:
        return self.MapOffset(duplicateOffset, WRITE_ON_HOT_MIN, WRITE_ON_HOT_MAX)

    # 根據覆蓋的範圍做標準化後映射到reward的範圍內回傳reward (應用在寫入到Hot資料時)
    def WriteOnCold(self, duplicateOffset: int) -> int:
        return self.MapOffset(duplicateOffset, WRITE_ON_COLD_MIN, WRITE_ON_COLD_MAX)

    # 根據覆蓋的範圍做標準化後映射到reward的範圍內回傳reward (應用在寫入到Hot資料時)
    def ReadOnHot(self, duplicateOffset: int) -> int:
        return self.MapOffset(duplicateOffset, READ_ON_HOT_MIN, READ_ON_HOT_MAX)

    # 根據覆蓋的範圍做標準化後映射到reward的範圍內回傳reward (應用在寫入到Hot資料時)
    def ReadOnCold(self, duplicateOffset: int) -> int:
        return self.MapOffset(duplicateOffset, READ_ON_COLD_MIN, READ_ON_COLD_MAX)
    
    # 將duplicateOffset根據標準化後的範圍map到新的min -> max中
    def MapOffset(self, duplicateOffset: int, newMin: int, newMax: int) -> int:
        duplicateOffsetScaled = self._scaler.transform([[duplicateOffset]])[0][0]
        dupRate = (duplicateOffsetScaled - self._min) / (self._max - self._min)
        mapResult = int(dupRate * (newMax - newMin) + newMin)
        return mapResult