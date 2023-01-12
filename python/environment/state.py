from collections import namedtuple
from .trace_loader import TraceLoader
from .tokenizer import FidTokenizer

State = namedtuple('State', ['trace', 'fid_token', 'lba_difference', 'num_bytes'])
class StateLoader:
    def __init__(self) -> None:
        self._traceLoader = TraceLoader()
        self._tokenizer = FidTokenizer()
        self._lastTrace = None 

    def ResetAll(self):
        self._traceLoader.ResetAll()
        self._tokenizer.ResetAll()
        self._lastTrace = None 

    def ResetEpisode(self):
        self._tokenizer.ResetAll()
        self._lastTrace = None

    def Load(self, path, length = -1):
        self._traceLoader.Load(path, length)

    def CountTraceDifference(self, trace):
        if self._lastTrace:
            return trace._lba - self._lastTrace._lba
        else:
            return 0

    def GetState(self):
        trace = self._traceLoader.GetWriteTrace()
        fid_token = self._tokenizer[trace._fid]
        lba_difference = self.CountTraceDifference(trace)
        state = State(trace=trace, fid_token=fid_token, lba_difference=lba_difference, num_bytes=trace._bytes)
        self._lastTrace = trace
        return state