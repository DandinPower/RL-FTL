from ..libs.logs import PrintLog
from ..environment.tokenizer import FidTokenizer
from dotenv import load_dotenv
from tqdm import tqdm
import pandas as pd 
import os
load_dotenv()

TARGET_ANSWER_PATH = os.getenv('TARGET_ANSWER_PATH')
INFERENCE_LENGTH = int(os.getenv('INFERENCE_LENGTH'))
MAX_STEP = int(os.getenv('MAX_STEP'))

class InferenceLoader:
    def __init__(self):
        self._tokenizer = FidTokenizer()
        self._X = []
        self._Y = []
        self._totalCount = 0
        self._count = 0
        self._lastLba = None

    def Reset(self):
        self._count = 0
        self._lastLba = None
        self._tokenizer.ResetAll()
        
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
            fid_token = self._tokenizer[int(row[1])]
            lba_difference = int(row[2]) - self._lastLba
            num_bytes = int(row[3])
            self._X.append((fid_token, lba_difference, num_bytes))
            if self._totalCount == totalLength:
                break