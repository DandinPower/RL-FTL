from python.libs.statistic import WriteEntry, Entries
from dotenv import load_dotenv
import os
load_dotenv()

LBA_SIZE = int(os.getenv('LBA_SIZE'))
PAGE_SIZE = 4096


def test_staticVariable_1():
    entry = WriteEntry(1,1,1, True)
    entry2 = WriteEntry(1,1,1, True)
    assert entry._id == 0
    assert entry2._id == 1

def test_entriesAdd_1():
    entries = Entries()
    entries.Add(1,0,1000, True)
    entries.Add(1,1001,10, True)
    assert len(entries._entries) == 0
    assert len(entries._notFinishEntries) == 2

def test_entriesAdd_2():
    entries = Entries()
    entries.Add(1,0,1000, True)
    entries.Add(1,999,10, True)
    assert len(entries._entries) == 1
    assert len(entries._notFinishEntries) == 1
    assert entries._entries[0]._type == True

def test_entriesAdd_3():
    entries = Entries()
    entries.Add(1,0,1000, True)
    assert len(entries._notFinishEntries) == 1
    entries.Add(1,1000000000,1000, True)
    assert len(entries._entries) == 0
    assert len(entries._notFinishEntries) == 2
    entries.Add(1,1001, LBA_SIZE * PAGE_SIZE, True)
    assert len(entries._entries) == 2
    assert len(entries._notFinishEntries) == 1
    assert entries._entries[0]._type == False
    assert entries._entries[1]._type == False

def test_entriesAdd_4():
    entries = Entries()
    entries.Add(1,0,1000, True)
    assert len(entries._notFinishEntries) == 1
    entries.Add(1,1000000000,1000, True)
    assert len(entries._entries) == 0
    assert len(entries._notFinishEntries) == 2
    entries.Add(1,1000000999, LBA_SIZE * PAGE_SIZE, True)
    assert len(entries._entries) == 2
    assert len(entries._notFinishEntries) == 1
    assert entries._entries[0]._type == False
    assert entries._entries[1]._type == True