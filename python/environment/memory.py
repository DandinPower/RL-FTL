from ..libs.cal import CompareTwoRange, GetTwoRangeIntersection
from trace import Trace

# 負責模擬現在的lba使用情況
class LogicAddress:
    def __init__(self, address: int, offset: int, type: bool) -> None:
        self._address = address
        self._offset = offset  
        self._type = type

    def SetOffset(self, offset: int) -> None:
        self._offset = offset

    # 檢查另一個Address有無重疊的部分
    def IsDuplicate(self, other: object):
        if not isinstance(other, LogicAddress):
            raise TypeError('Invalid Type: Not LogicAddress')
        return CompareTwoRange(self._address, self._address + self._offset, other._address, other._address + other._offset)
    
    # 回傳重疊的大小
    def GetDuplicate(self, other:object):
        if not isinstance(other, LogicAddress):
            raise TypeError('Invalid Type: Not LogicAddress')
        return GetTwoRangeIntersection(self._address, self._address + self._offset, other._address, other._address + other._offset)

    # 檢查兩個Address是否完全一樣
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, LogicAddress):
            return (self._address == __o._address) and (self._offset == __o._offset) and (self._type == __o._type)
        return False 

    # print 時顯示的字元
    def __str__(self) -> str:
        return f'[LogicAddress]Address: {self._address}, Offset: {self._offset}, Type: {self._type}'

    # print 時顯示的字元
    def __repr__(self) -> str:
        return f'[LogicAddress]Address: {self._address}, Offset: {self._offset}, Type: {self._type}'

    # 定義好比較的定義來讓原生的Sort可以運作
    def __lt__(self, other):
        if self._address <= other._address:
            return True
        elif self._address > other._address:
            return False

class LogicMemory:
    def __init__(self):
        self.bits = list()  # set of LogicBits

    # 檢查memory address 數量
    def GetLength(self) -> int:
        return len(self.bits)

    # 檢查address是否存在
    def CheckAddressIsExist(self, address: LogicAddress) -> bool:
        for item in self.bits:
            if item == address:
                return True
        return False

    # 檢查有無重複的address
    def CheckDuplication(self) -> None:
        table = set()
        for item in self.bits:
            if item._address in table:
                return True
            table.add(item._address)
        return False

    # 處理重疊的address
    def HandleDuplicateAddress(self, originalAddress: LogicAddress, newAddress: LogicAddress) -> None:
        originalStart = originalAddress._address
        originalEnd = originalAddress._address + originalAddress._offset
        newStart = newAddress._address
        newEnd = newAddress._address + newAddress._offset
        if originalStart < newStart:
            if newEnd >= originalEnd:
                self.bits.append(LogicAddress(originalStart, newStart - originalStart, originalAddress._type))
            else:
                self.bits.append(LogicAddress(originalStart, newStart - originalStart, originalAddress._type))
                self.bits.append(LogicAddress(newEnd, originalEnd - newEnd, originalAddress._type))
        else:
            if newEnd < originalEnd:
                self.bits.append(LogicAddress(newEnd, originalEnd - newEnd, originalAddress._type))

    # 將一筆trace寫進memory 並回傳duplicate的offset
    def WriteTrace(self, trace: Trace, type: bool) -> tuple:
        newLogicAddress = LogicAddress(trace._lba, trace._bytes, type)
        prepareRemoveAddress = []
        hotDuplicateOffset = 0
        coldDuplicateOffset = 0
        for i in range(len(self.bits)):
            tempOriginalLogicAddress = self.bits[i]
            if tempOriginalLogicAddress.IsDuplicate(newLogicAddress):
                self.HandleDuplicateAddress(tempOriginalLogicAddress, newLogicAddress)
                prepareRemoveAddress.append(tempOriginalLogicAddress)
                if tempOriginalLogicAddress._type == True:
                    hotDuplicateOffset += tempOriginalLogicAddress.GetDuplicate(newLogicAddress)
                else:
                    coldDuplicateOffset += tempOriginalLogicAddress.GetDuplicate(newLogicAddress)
        for i in range(len(prepareRemoveAddress)):
            self.bits.remove(prepareRemoveAddress[i])
        self.bits.append(newLogicAddress)
        #if self.CheckDuplication():
        #    raise MemoryError('Address Duplicate')
        return (hotDuplicateOffset, coldDuplicateOffset)

    # 讀取一筆trace進memory
    def ReadTrace(self, trace: Trace) -> tuple:
        newLogicAddress = LogicAddress(trace._lba, trace._bytes, None)
        hotDuplicateOffset = 0
        coldDuplicateOffset = 0
        for tempOriginalLogicAddress in self.bits:
            if tempOriginalLogicAddress.IsDuplicate(newLogicAddress):
                if tempOriginalLogicAddress._type == True:
                        hotDuplicateOffset += tempOriginalLogicAddress.GetDuplicate(newLogicAddress)
                else:
                    coldDuplicateOffset += tempOriginalLogicAddress.GetDuplicate(newLogicAddress)
        return (hotDuplicateOffset, coldDuplicateOffset) 

    # 根據address來排列bits 
    def Sort(self) -> None:
        self.bits = sorted(self.bits)

    # print 時顯示的字元
    def __str__(self) -> str:
        output = ''
        for item in self.bits:
            output += f'[LogicAddress]Address: {item._address}, Offset: {item._offset}, Type: {item._type}\n'
        return output