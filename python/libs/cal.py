def CompareTwoRange(x1: int, x2: int, y1: int, y2: int) -> bool:
    print(x1, x2, y1, y2)
    if y1 >= x2 or y2 <= x1:
        return False 
    return True