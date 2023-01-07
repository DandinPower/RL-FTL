def CompareTwoRange(x1: int, x2: int, y1: int, y2: int) -> bool:
    if (x1 >= y1 and x1 < y2) or (y1 >= x1 and y1 < x2):
        return True
    return False

# 回傳兩個range交集的長度
def GetTwoRangeIntersection(x1: int, x2: int, y1: int, y2: int) -> int:
    start = max(x1, y1)
    end = min(x2, y2)
    return end - start
