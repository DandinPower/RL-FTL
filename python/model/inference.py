from ..libs.logs import PrintLog
from ..environment.tokenizer import FidTokenizer, RangeTokenizer, FrequencyTokenizer
from dotenv import load_dotenv
from tqdm import tqdm
import pandas as pd 
import os
load_dotenv()

TARGET_ANSWER_PATH = os.getenv('TARGET_ANSWER_PATH')
INFERENCE_LENGTH = int(os.getenv('INFERENCE_LENGTH'))
MAX_STEP = int(os.getenv('MAX_STEP'))

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

class InferenceLoader:
    def __init__(self):
        self._fidFreqTokenizer = FrequencyTokenizer(FID_FREQUENCY_SAMPLE_SIZE, FID_FREQUENCY_SAMPLE_RANGE)
        self._lbaDiffRangeTokenizer = RangeTokenizer(LBA_DIFF_SAMPLE_0, LBA_DIFF_SAMPLE_1, LBA_DIFF_SAMPLE_2)
        self._numBytesRangeTokenizer = RangeTokenizer(NUM_BYTES_SAMPLE_0, NUM_BYTES_SAMPLE_1, NUM_BYTES_SAMPLE_2)
        self._biggerThanLbaRangeTokenizer = RangeTokenizer(NUM_BYTES_BIGGER_THAN_LBA)
        self._X = []
        self._Y = []
        self._totalCount = 0
        self._count = 0
        self._lastLba = None

    def Reset(self):
        self._count = 0
        self._lastLba = None
        self._fidFreqTokenizer.ResetAll()
        
    def Load(self):
        PrintLog('use pandas to read target csv....')
        df = pd.read_csv(TARGET_ANSWER_PATH, header = None, delimiter=',', lineterminator='\n')
        if INFERENCE_LENGTH > len(df): totalLength = len(df)
        else: totalLength = INFERENCE_LENGTH
        for index, row in tqdm(df.iterrows(), total = totalLength):
            self._totalCount += 1
            if self._count == MAX_STEP:
                self.Reset()
            self._count += 1
            if self._count == 1:
                self._lastLba = int(row[2])
                continue
            self._Y.append(row[4] == 'hot')

            fid_freq_token = self._fidFreqTokenizer[int(row[1])]
            lba_diff = int(row[2]) - self._lastLba
            lba_difference_range_token = self._lbaDiffRangeTokenizer[lba_diff]
            num_bytes_range_token = self._numBytesRangeTokenizer[int(row[3])]
            num_bytes_bigger_than_lba_range_token = self._biggerThanLbaRangeTokenizer[int(row[3])]
            self._X.append((fid_freq_token, lba_difference_range_token, num_bytes_range_token, num_bytes_bigger_than_lba_range_token))
            if self._totalCount == totalLength:
                break