import pandas as pd 
import csv 
from tqdm import tqdm
import os
from ..libs.logs import PrintLog
from dotenv import load_dotenv
load_dotenv()

TARGET_ANSWER_PATH = os.getenv('TARGET_ANSWER_PATH')

def LoadAnswerToXY():
    PrintLog('use pandas to read csv....')
    X = []
    Y = []
    df = pd.read_csv(TARGET_ANSWER_PATH, header = None, delimiter=',', lineterminator='\n')
    for index, row in tqdm(df.iterrows(), total = len(df)):
        Y.append(row[4] == 'hot')
        #X.append(row[:3])
        # 運用state loader來讀取X資料 需要進行tokenizer(每一個Max_step重算一次)跟lba_difference的作業