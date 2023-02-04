from python.environment.tokenizer import RangeTokenizer, FrequencyTokenizer
from dotenv import load_dotenv
import os
load_dotenv()

LBA_DIFF_SAMPLE_0 = int(os.getenv('LBA_DIFF_SAMPLE_0'))
LBA_DIFF_SAMPLE_1 = int(os.getenv('LBA_DIFF_SAMPLE_1'))
LBA_DIFF_SAMPLE_2 = int(os.getenv('LBA_DIFF_SAMPLE_2'))
FID_FREQUENCY_SAMPLE_SIZE = int(os.getenv('FID_FREQUENCY_SAMPLE_SIZE'))
FID_FREQUENCY_SAMPLE_RANGE = int(os.getenv('FID_FREQUENCY_SAMPLE_RANGE'))

def test_RangeTokenizer_1():
    tokenizer = RangeTokenizer(LBA_DIFF_SAMPLE_0, LBA_DIFF_SAMPLE_1, LBA_DIFF_SAMPLE_2)
    assert 0 == tokenizer[LBA_DIFF_SAMPLE_0 - 1]
    assert 0 == tokenizer[-(LBA_DIFF_SAMPLE_0 - 1)]
    assert 0 == tokenizer[0]
    assert 0 == tokenizer[LBA_DIFF_SAMPLE_0]
    assert 0 == tokenizer[-LBA_DIFF_SAMPLE_0]
    assert 1 == tokenizer[LBA_DIFF_SAMPLE_0 + 1]
    assert 1 == tokenizer[-(LBA_DIFF_SAMPLE_0 + 1)]
    assert 1 == tokenizer[LBA_DIFF_SAMPLE_1]
    assert 1 == tokenizer[-LBA_DIFF_SAMPLE_1]
    assert 2 == tokenizer[LBA_DIFF_SAMPLE_1 + 1]
    assert 2 == tokenizer[-(LBA_DIFF_SAMPLE_1 + 1)]
    assert 2 == tokenizer[LBA_DIFF_SAMPLE_2]
    assert 2 == tokenizer[-LBA_DIFF_SAMPLE_2]
    assert 3 == tokenizer[LBA_DIFF_SAMPLE_2 + 1]
    assert 3 == tokenizer[-(LBA_DIFF_SAMPLE_2 + 1)]
    assert 3 == tokenizer[LBA_DIFF_SAMPLE_2 * 2]
    assert 3 == tokenizer[-(LBA_DIFF_SAMPLE_2 * 2)]

def test_FrequencyTokenizer_1():
    tokenizer = FrequencyTokenizer(FID_FREQUENCY_SAMPLE_SIZE, FID_FREQUENCY_SAMPLE_RANGE)
    for i in range(FID_FREQUENCY_SAMPLE_RANGE):
        assert i == tokenizer[1234]
    assert FID_FREQUENCY_SAMPLE_RANGE - 1 == tokenizer[1234]