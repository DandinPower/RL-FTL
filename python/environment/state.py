from collections import namedtuple
from .trace_loader import TraceLoader
from .tokenizer import FidTokenizer, RangeTokenizer, FrequencyTokenizer
from dotenv import load_dotenv
import os
load_dotenv()

FID_FREQUENCY_SAMPLE_SIZE = int(os.getenv('FID_FREQUENCY_SAMPLE_SIZE'))
FID_FREQUENCY_SAMPLE_RANGE = int(os.getenv('FID_FREQUENCY_SAMPLE_RANGE'))
LBA_DIFF_SAMPLE_0 = int(os.getenv('LBA_DIFF_SAMPLE_0'))
LBA_DIFF_SAMPLE_1 = int(os.getenv('LBA_DIFF_SAMPLE_1'))
LBA_DIFF_SAMPLE_2 = int(os.getenv('LBA_DIFF_SAMPLE_2'))
LBA_DIFF_SAMPLE_RANGE = int(os.getenv('LBA_DIFF_SAMPLE_RANGE'))
NUM_BYTES_SAMPLE_0 = int(os.getenv('NUM_BYTES_SAMPLE_0'))
NUM_BYTES_SAMPLE_1 = int(os.getenv('NUM_BYTES_SAMPLE_1'))
NUM_BYTES_SAMPLE_2 = int(os.getenv('NUM_BYTES_SAMPLE_2'))
NUM_BYTES_SAMPLE_RANGE = int(os.getenv('NUM_BYTES_SAMPLE_RANGE'))
NUM_BYTES_BIGGER_THAN_LBA = int(os.getenv('NUM_BYTES_BIGGER_THAN_LBA'))
NUM_BYTES_BIGGER_THAN_LBA_RANGE = int(os.getenv('NUM_BYTES_BIGGER_THAN_LBA_RANGE'))

State = namedtuple('State', ['trace', 'fid_freq_token', 'lba_difference_range_token', 'num_bytes_range_token', 'num_bytes_bigger_than_lba_range_token'])

class StateLoader:
    def __init__(self) -> None:
        self._traceLoader = TraceLoader()
        self._fidFreqTokenizer = FrequencyTokenizer(FID_FREQUENCY_SAMPLE_SIZE, FID_FREQUENCY_SAMPLE_RANGE)
        self._lbaDiffRangeTokenizer = RangeTokenizer(LBA_DIFF_SAMPLE_0, LBA_DIFF_SAMPLE_1, LBA_DIFF_SAMPLE_2)
        self._numBytesRangeTokenizer = RangeTokenizer(NUM_BYTES_SAMPLE_0, NUM_BYTES_SAMPLE_1, NUM_BYTES_SAMPLE_2)
        self._biggerThanLbaRangeTokenizer = RangeTokenizer(NUM_BYTES_BIGGER_THAN_LBA)
        self._lastTrace = None

    def ResetAll(self):
        self._traceLoader.ResetAll()
        self._fidFreqTokenizer.ResetAll()
        self._lastTrace = None 

    def ResetEpisode(self):
        self._fidFreqTokenizer.ResetAll()
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
        fid_freq_token = self._fidFreqTokenizer[trace._fid]
        lba_diff = self.CountTraceDifference(trace)
        lba_difference_range_token = self._lbaDiffRangeTokenizer[lba_diff]
        num_bytes_range_token = self._numBytesRangeTokenizer[trace._bytes]
        num_bytes_bigger_than_lba_range_token = self._biggerThanLbaRangeTokenizer[trace._bytes]
        state = State(trace = trace, fid_freq_token = fid_freq_token, lba_difference_range_token = lba_difference_range_token, num_bytes_range_token = num_bytes_range_token, num_bytes_bigger_than_lba_range_token = num_bytes_bigger_than_lba_range_token)
        self._lastTrace = trace
        return state

    def Preprocess(self, state):
        fid_freq_token = state[1]
        lba_difference_range_token = state[2]
        num_bytes_range_token = state[3]
        num_bytes_bigger_than_lba_range_token = state[4]
        return (fid_freq_token, lba_difference_range_token, num_bytes_range_token, num_bytes_bigger_than_lba_range_token)