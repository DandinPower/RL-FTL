from ..libs.cal import CompareTwoRange

class Trace:
    def __init__(self, opCode, fid, lba, bytes):
        self._opCode = opCode 
        self._fid = fid 
        self._lba = lba 
        self._bytes = bytes 
    
    def __str__(self):
        return f'Trace: OpCode {self._opCode}, Fid {self._fid}, Lba {self._lba}, Bytes {self._bytes}'