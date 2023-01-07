from python.environment.memory import LogicMemory
from python.environment.memory import LogicAddress
from python.environment.trace import Trace

def test_LogicMemoryConflict_1():
    traceA = Trace(-1, -1, 0, 10)
    traceB = Trace(-1, -1, 5, 10)
    memory = LogicMemory()
    memory.WriteTrace(traceA, True)
    memory.WriteTrace(traceB, False)
    addressA = LogicAddress(0, 5, True)
    addressB = LogicAddress(5, 10, False)
    assert memory.CheckAddressIsExist(addressA) == True
    assert memory.CheckAddressIsExist(addressB) == True
    assert memory.GetLength() == 2

def test_LogicMemoryConflict_2():
    traceA = Trace(-1, -1, 0, 10)
    traceB = Trace(-1, -1, 5, 5)
    memory = LogicMemory()
    memory.WriteTrace(traceA, True)
    memory.WriteTrace(traceB, False)
    addressA = LogicAddress(0, 5, True)
    addressB = LogicAddress(5, 5, False)
    assert memory.CheckAddressIsExist(addressA) == True
    assert memory.CheckAddressIsExist(addressB) == True
    assert memory.GetLength() == 2

def test_LogicMemoryConflict_3():
    traceA = Trace(-1, -1, 0, 10)
    traceB = Trace(-1, -1, 5, 3)
    memory = LogicMemory()
    memory.WriteTrace(traceA, True)
    memory.WriteTrace(traceB, False)
    addressA = LogicAddress(0, 5, True)
    addressB = LogicAddress(5, 3, False)
    addressC = LogicAddress(8, 2, True)
    assert memory.CheckAddressIsExist(addressA) == True
    assert memory.CheckAddressIsExist(addressB) == True
    assert memory.CheckAddressIsExist(addressC) == True
    assert memory.GetLength() == 3

def test_LogicMemoryConflict_4():
    traceA = Trace(-1, -1, 0, 10)
    traceB = Trace(-1, -1, 0, 5)
    memory = LogicMemory()
    memory.WriteTrace(traceA, True)
    memory.WriteTrace(traceB, False)
    addressA = LogicAddress(0, 5, False)
    addressB = LogicAddress(5, 5, True)
    assert memory.CheckAddressIsExist(addressA) == True
    assert memory.CheckAddressIsExist(addressB) == True
    assert memory.GetLength() == 2

def test_LogicMemoryConflict_5():
    traceA = Trace(-1, -1, 0, 10)
    traceB = Trace(-1, -1, 0, 10)
    memory = LogicMemory()
    memory.WriteTrace(traceA, True)
    memory.WriteTrace(traceB, False)
    addressA = LogicAddress(0, 10, False)
    assert memory.CheckAddressIsExist(addressA) == True
    assert memory.GetLength() == 1

def test_LogicMemoryConflict_6():
    traceA = Trace(-1, -1, 0, 10)
    traceB = Trace(-1, -1, 0, 12)
    memory = LogicMemory()
    memory.WriteTrace(traceA, True)
    memory.WriteTrace(traceB, False)
    addressA = LogicAddress(0, 12, False)
    assert memory.CheckAddressIsExist(addressA) == True
    assert memory.GetLength() == 1

def test_LogicMemoryConflict_7():
    traceA = Trace(-1, -1, 2, 10)
    traceB = Trace(-1, -1, 0, 10)
    memory = LogicMemory()
    memory.WriteTrace(traceA, True)
    memory.WriteTrace(traceB, False)
    addressA = LogicAddress(0, 10, False)
    addressB = LogicAddress(10, 2, True)
    assert memory.CheckAddressIsExist(addressA) == True
    assert memory.CheckAddressIsExist(addressB) == True
    assert memory.GetLength() == 2

def test_LogicMemoryConflict_8():
    traceA = Trace(-1, -1, 2, 8)
    traceB = Trace(-1, -1, 0, 10)
    memory = LogicMemory()
    memory.WriteTrace(traceA, True)
    memory.WriteTrace(traceB, False)
    addressA = LogicAddress(0, 10, False)
    assert memory.CheckAddressIsExist(addressA) == True
    assert memory.GetLength() == 1

def test_LogicMemoryConflict_9():
    traceA = Trace(-1, -1, 2, 8)
    traceB = Trace(-1, -1, 0, 12)
    memory = LogicMemory()
    memory.WriteTrace(traceA, True)
    memory.WriteTrace(traceB, False)
    addressA = LogicAddress(0, 12, False)
    assert memory.CheckAddressIsExist(addressA) == True
    assert memory.GetLength() == 1

def test_LogicMemoryConflict_10():
    traceA = Trace(-1, -1, 0, 10)
    traceB = Trace(-1, -1, 12, 4)
    traceC = Trace(-1, -1, 2, 12)
    memory = LogicMemory()
    memory.WriteTrace(traceA, True)
    memory.WriteTrace(traceB, True)
    memory.WriteTrace(traceC, False)
    addressA = LogicAddress(0, 2, True)
    addressB = LogicAddress(2, 12, False)
    addressC = LogicAddress(14, 2, True)
    assert memory.CheckAddressIsExist(addressA) == True
    assert memory.CheckAddressIsExist(addressB) == True
    assert memory.CheckAddressIsExist(addressC) == True
    assert memory.GetLength() == 3

def test_LogicMemoryConflict_11():
    traceA = Trace(-1, -1, 0, 10)
    traceB = Trace(-1, -1, 12, 4)
    traceC = Trace(-1, -1, 2, 9)
    memory = LogicMemory()
    memory.WriteTrace(traceA, True)
    memory.WriteTrace(traceB, True)
    memory.WriteTrace(traceC, False)
    addressA = LogicAddress(0, 2, True)
    addressB = LogicAddress(2, 9, False)
    addressC = LogicAddress(12, 4, True)
    assert memory.CheckAddressIsExist(addressA) == True
    assert memory.CheckAddressIsExist(addressB) == True
    assert memory.CheckAddressIsExist(addressC) == True
    assert memory.GetLength() == 3

def test_LogicMemoryConflict_12():
    traceA = Trace(-1, -1, 0, 10)
    traceB = Trace(-1, -1, 12, 4)
    traceC = Trace(-1, -1, 2, 15)
    memory = LogicMemory()
    memory.WriteTrace(traceA, True)
    memory.WriteTrace(traceB, True)
    memory.WriteTrace(traceC, False)
    addressA = LogicAddress(0, 2, True)
    addressB = LogicAddress(2, 15, False)
    assert memory.CheckAddressIsExist(addressA) == True
    assert memory.CheckAddressIsExist(addressB) == True
    assert memory.GetLength() == 2

def test_LogicMemoryConflict_13():
    traceA = Trace(-1, -1, 0, 4)
    traceB = Trace(-1, -1, 6, 4)
    traceC = Trace(-1, -1, 5, 3)
    memory = LogicMemory()
    memory.WriteTrace(traceA, True)
    memory.WriteTrace(traceB, True)
    memory.WriteTrace(traceC, False)
    addressA = LogicAddress(0, 4, True)
    addressB = LogicAddress(8, 2, True)
    addressC = LogicAddress(5, 3, False)
    assert memory.CheckAddressIsExist(addressA) == True
    assert memory.CheckAddressIsExist(addressB) == True
    assert memory.CheckAddressIsExist(addressC) == True
    assert memory.GetLength() == 3

def test_LogicMemoryConflict_14():
    traceA = Trace(-1, -1, 2, 2)
    traceB = Trace(-1, -1, 6, 4)
    traceC = Trace(-1, -1, 0, 8)
    memory = LogicMemory()
    memory.WriteTrace(traceA, True)
    memory.WriteTrace(traceB, True)
    memory.WriteTrace(traceC, False)
    addressA = LogicAddress(8, 2, True)
    addressB = LogicAddress(0, 8, False)
    assert memory.CheckAddressIsExist(addressA) == True
    assert memory.CheckAddressIsExist(addressB) == True
    assert memory.GetLength() == 2