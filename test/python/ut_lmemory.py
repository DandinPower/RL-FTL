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