from ..libs.cal import CompareTwoRange
from trace import Trace

# 負責模擬現在的lba使用情況
class LogicAddress:
    def __init__(self, address: int, offset: int, type: bool) -> None:
        self._address = address
        self._offset = offset  
        self._type = type

    def SetOffset(self, offset: int) -> None:
        self._offset = offset

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, LogicAddress):
            return (self._address == __o._address) and (self._offset == __o._offset) and (self._type == __o._type)
        return False 
    
    def IsDuplicate(self, other: object):
        if not isinstance(other, LogicAddress):
            raise TypeError('Invalid Type: Not LogicAddress')
        return CompareTwoRange(self._address, self._address + self._offset, other._address, other._address + other._offset)

    def __str__(self) -> str:
        return f'Address: {self._address}, Offset: {self._offset}, Type: {self._type}'

    def __repr__(self) -> str:
        return f'Address: {self._address}, Offset: {self._offset}, Type: {self._type}'

    def __lt__(self, other):
        if self._address <= other._address:
            return True
        elif self._address > other._address:
            return False

class LogicMemory:
    def __init__(self):
        self.bits = list()  # set of LogicBits

    # 處理重疊的address
    def HandleDuplicateAddress(self, originalAddress: LogicAddress, newAddress: LogicAddress) -> None:
        originalStart = originalAddress._address
        originalEnd = originalAddress._address + originalAddress._offset
        newStart = newAddress._address
        newEnd = newAddress._address + newAddress._offset
        if originalStart < newStart:
            if newEnd >= originalEnd:
                self.bits.append(LogicAddress(originalStart, newStart - originalStart, originalAddress._type))
                self.bits.append(newAddress)
            else:
                self.bits.append(LogicAddress(originalStart, newStart - originalStart, originalAddress._type))
                self.bits.append(newAddress)
                self.bits.append(LogicAddress(newEnd, originalEnd - newEnd, originalAddress._type))
        else:
            if newEnd < originalEnd:
                self.bits.append(newAddress)
                self.bits.append(LogicAddress(newEnd, originalEnd - newEnd, originalAddress._type))
            elif newEnd >= originalEnd:
                self.bits.append(newAddress)

    # 將一筆trace寫進memory
    def WriteTrace(self, trace: Trace, type: bool) -> None:
        tempLogicAddress = LogicAddress(trace._lba, trace._bytes, type)
        check = False
        removeIndex = -1
        for i in range(len(self.bits)):
            originalAddress = self.bits[i]
            if originalAddress.IsDuplicate(tempLogicAddress):
                self.HandleDuplicateAddress(originalAddress, tempLogicAddress)
                removeIndex = i
                check = True
                break
        if check:
            self.bits.pop(removeIndex)
        else:
            self.bits.append(tempLogicAddress)
    
    # 檢查address是否存在
    def CheckAddressIsExist(self, address: LogicAddress) -> bool:
        for item in self.bits:
            if item == address:
                return True
        return False
    
    # 檢查memory address 數量
    def GetLength(self) -> int:
        return len(self.bits)
    
    # 根據address來排列bits 
    def Sort(self) -> None:
        self.bits = sorted(self.bits)

    # 檢查有無重複的address
    def CheckDuplication(self) -> None:
        table = set()
        for item in self.bits:
            if item._address in table:
                return True
            table.add(item._address)
        return False