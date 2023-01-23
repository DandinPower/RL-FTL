from .cal import CompareTwoRange
from dotenv import load_dotenv
import csv
import os
load_dotenv()

LBA_SIZE = int(os.getenv('LBA_SIZE'))
PAGE_SIZE = 4096

class WriteEntry:
    increment_id = 0
    def __init__(self, fid, address, offset) -> None:
        self._fid = fid
        self._address = address
        self._offset = offset  
        self._id = WriteEntry.increment_id
        self._type = False
        self._free = LBA_SIZE * PAGE_SIZE
        self.__class__.increment_id += 1
    
    # 檢查另一個Address有無重疊的部分
    def IsDuplicate(self, other: object):
        if not isinstance(other, WriteEntry):
            raise TypeError('Invalid Type: Not WriteEntry')
        return CompareTwoRange(self._address, self._address + self._offset, other._address, other._address + other._offset)

    def IsAvailable(self) -> bool:
        return self._free > 0

    def NewEntry(self, other: object):
        if self._free <= 0:
            raise RuntimeError('entry is already made an decision')
        self._free -= other._offset
        if self.IsDuplicate(other):
            self._type = True 
            self._free = 0
    
    # 定義好比較的定義來讓原生的Sort可以運作
    def __lt__(self, other):
        if self._id <= other._id:
            return True
        elif self._id > other._id:
            return False
        
    def Tuple(self):
        type = 'cold'
        if self._type:
            type = 'hot'
        return (self._id, self._fid, self._address, self._offset, type, self._free)

class Entries:
    def __init__(self) -> None:
        self._entries = []
        self._notFinishEntries = []

    def Add(self, fid, address, offset):
        tempEntry = WriteEntry(fid, address, offset)
        removeList = []
        for entry in self._notFinishEntries:
            entry.NewEntry(tempEntry)
            if not entry.IsAvailable():
                removeList.append(entry)
        for entry in removeList:
            self._notFinishEntries.remove(entry)
            self._entries.append(entry)
        self._notFinishEntries.append(tempEntry)

    def Write(self, path):
        tempResult = []
        tempResult.extend(self._entries)
        tempResult.extend(self._notFinishEntries)
        tempResult.sort()
        tempResult = [entry.Tuple() for entry in tempResult]
        with open(path, 'w', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(tempResult)
