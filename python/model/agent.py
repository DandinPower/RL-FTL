from ..environment.trace_loader import TraceLoader
from ..environment.environment import Environment
from ..environment.memory import LogicMemory
from tqdm import tqdm
import random

def main():
    environment = Environment()
    memory = LogicMemory()
    environment.SetMemory(memory)
    traceLoader = TraceLoader()
    traceLoader.Load('trace/TPCC.trace.csv', 10000)
    for i in tqdm(range(10000)):
    #for i in tqdm(range(traceLoader.GetLength())):
        environment.Step(traceLoader.GetTrace(), random.choice([True, False]))
    memory.Sort()
    for item in memory.bits:
        print(item)
    if memory.CheckDuplication():
        print('Duplicate!')

if __name__ == "__main__":
    main()