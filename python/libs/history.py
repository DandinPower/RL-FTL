from dotenv import load_dotenv
import csv
import os
load_dotenv()

TRACE_DUPLICATE_OFFSET_MAX = int(os.getenv('TRACE_DUPLICATE_OFFSET_MAX'))
TRACE_DUPLICATE_OFFSET_MIN = int(os.getenv('TRACE_DUPLICATE_OFFSET_MIN'))

class History:
    def __init__(self):
        self.datas = dict()

    def IsGreaterThanMin(x):
        return x >= TRACE_DUPLICATE_OFFSET_MIN
    
    def IsLowerThanMax(x):
        return x <= TRACE_DUPLICATE_OFFSET_MAX

    def Step(self, x):
        if x > 0:
            if self.datas.get(x) == None:
                self.datas[x] = 1
            else:
                self.datas[x] = self.datas.get(x) + 1

    def Sort(self):
        self.datas = {k: self.datas[k] for k in sorted(self.datas)}

    def Show(self):
        for key, value in self.datas.items():
            print(f'duplicate: {key}, nums: {value}')
        
    def Write(self, path):
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for key, value in self.datas.items():
                writer.writerow([key, value])
