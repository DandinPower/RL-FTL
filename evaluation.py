from python.libs.statistic import Entries
from python.environment.trace_loader import TraceLoader
from dotenv import load_dotenv
import os
load_dotenv()

TRACE_FILE_PATH = os.getenv('TRACE_FILE_PATH')
TRACE_LOAD_LENGTH = int(os.getenv('TRACE_LOAD_LENGTH'))

LBA_SIZE = int(os.getenv('LBA_SIZE'))
PAGE_SIZE = 4096

def main():
    traceLoader = TraceLoader()
    traceLoader.Load(TRACE_FILE_PATH, TRACE_LOAD_LENGTH)
    entries = Entries()
    for i in range(len(traceLoader)):
        trace = traceLoader.GetWriteTrace()
        entries.Add(trace._fid, trace._lba, trace._bytes)
    entries.Write('python/history/statistic_evaluation.csv')

if __name__ == "__main__":
    main()