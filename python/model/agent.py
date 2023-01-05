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
    traceLoader.Load('trace/TPCC.trace.csv', 1000)
    for i in tqdm(range(100)):
    #for i in tqdm(range(traceLoader.GetLength())):
        environment.Step(traceLoader.GetTrace(), random.choice([True, False]))
    print(len(memory.bits.items()))
    for key, value in memory.bits.items():
        print(f'address: {key}, value: {value}')

if __name__ == "__main__":
    main()