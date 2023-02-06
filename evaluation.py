from python.libs.statistic import Entries
from python.model.agent import Agent, InferenceAgent
from python.environment.trace_loader import TraceLoader
from python.environment.tokenizer import FidTokenizer
from dotenv import load_dotenv
import os
load_dotenv()

TARGET_ANSWER_PATH = os.getenv('TARGET_ANSWER_PATH')
TRACE_FILE_PATH = os.getenv('TRACE_FILE_PATH')
TRACE_LOAD_LENGTH = int(os.getenv('TRACE_LOAD_LENGTH'))
LBA_SIZE = int(os.getenv('LBA_SIZE'))
PAGE_SIZE = 4096

class Counter:
    def __init__(self):
        self.datas = dict()
    
    def Add(self, value):
        value = abs(value)
        if self.datas.get(value) == None:
            self.datas[value] = 1
        else:
            self.datas[value] = self.datas.get(value) + 1

    def Show(self):
        for key in sorted(self.datas):
            print(f"{key}: {self.datas[key]}")

    def Write(self, path):
        with open(path, "w") as file:
            for key in sorted(self.datas):
                file.write(f"{key}: {self.datas[key]}\n")

def CheckLBADIFF():
    traceLoader = TraceLoader()
    traceLoader.Load(TRACE_FILE_PATH, TRACE_LOAD_LENGTH)
    tempLba = 0
    counter = Counter()
    for i in range(len(traceLoader)):
        trace = traceLoader.GetWriteTrace()
        lbadiff = trace._lba - tempLba
        tempLba = trace._lba
        counter.Add(lbadiff)
    counter.Write('python/history/lba_difference.txt')

def CheckBytes():
    traceLoader = TraceLoader()
    traceLoader.Load(TRACE_FILE_PATH, TRACE_LOAD_LENGTH)
    counter = Counter()
    for i in range(len(traceLoader)):
        trace = traceLoader.GetWriteTrace()
        counter.Add(trace._bytes)
    counter.Write('python/history/num_bytes.txt')


def CheckFidFrequency():
    traceLoader = TraceLoader()
    tokenizer = FidTokenizer()
    traceLoader.Load(TRACE_FILE_PATH, TRACE_LOAD_LENGTH)
    for i in range(len(traceLoader)):
        trace = traceLoader.GetWriteTrace()
        token = tokenizer[trace._fid]
        if i % 999 == 0:
            for key, value in tokenizer.datas.items():
                print(f'fid: {key}, id: {value.id}, count: {value.count}')
            print('//////////////////////')
            tokenizer.ResetAll()
    #print(tokenizer.datas)

def GetTargetAnswer():
    traceLoader = TraceLoader()
    traceLoader.Load(TRACE_FILE_PATH, TRACE_LOAD_LENGTH)
    entries = Entries()
    for i in range(len(traceLoader)):
        trace = traceLoader.GetWriteTrace()
        entries.Add(trace._fid, trace._lba, trace._bytes)
    entries.Write(TARGET_ANSWER_PATH)

def main():
    agent = InferenceAgent()
    agent.Inference()
    #CheckFidFrequency()
    #CheckLBADIFF()
    #CheckBytes()

if __name__ == "__main__":
    main()