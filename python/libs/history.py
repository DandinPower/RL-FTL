from ..environment.trace import Trace
from collections import namedtuple
import csv

Record = namedtuple('Record', ['op_code', 'fid', 'lba', 'num_bytes', 'action', 'reward'])

class History:
    def __init__(self):
        self.records = [] 
    
    def Add(self, trace, action, reward):
        opcode = trace._opCode
        fid = trace._fid
        lba = trace._lba
        num_bytes = trace._bytes
        if action == None:
            type = 'None'
        else:
            type = 'hot' if action else 'cold'
        self.records.append(Record(opcode, fid, lba, num_bytes, type, reward))
    
    def WriteHistory(self, path):
        with open(path, 'w', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(self.records)

    def __len__(self):
        return len(self.records)
