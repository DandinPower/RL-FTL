from python.environment.memory import LogicAddress

def test_LogicAddressEqual_1():
    a = LogicAddress(1, 2, True)
    b = LogicAddress(4, 2, True)
    assert a.IsDuplicate(b) == False

def test_LogicAddressEqual_2():
    a = LogicAddress(1, 2, True)
    b = LogicAddress(3, 2, True)
    assert a.IsDuplicate(b) == False

def test_LogicAddressEqual_3():
    a = LogicAddress(1, 2, True)
    b = LogicAddress(2, 2, True)
    assert a.IsDuplicate(b) == True

def test_LogicAddressEqual_4():
    a = LogicAddress(1, 2, True)
    b = LogicAddress(1, 2, True)
    assert a.IsDuplicate(b) == True

def test_LogicAddressEqual_5():
    a = LogicAddress(2, 2, True)
    b = LogicAddress(1, 2, True)
    assert a.IsDuplicate(b) == True

def test_LogicAddressEqual_6():
    a = LogicAddress(3, 2, True)
    b = LogicAddress(1, 2, True)
    assert a.IsDuplicate(b) == False

def test_LogicAddressEqual_7():
    a = LogicAddress(4, 2, True)
    b = LogicAddress(1, 2, True)
    assert a.IsDuplicate(b) == False

def test_LogicAddressEqual_8():
    a = LogicAddress(1, 4, True)
    b = LogicAddress(2, 2, True)
    assert a.IsDuplicate(b) == True

def test_LogicAddressEqual_9():
    a = LogicAddress(2, 2, True)
    b = LogicAddress(1, 4, True)
    assert a.IsDuplicate(b) == True