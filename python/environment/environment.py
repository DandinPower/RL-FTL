from .memory import LogicMemory

# 負責記錄整個環境
class Environment:
    def __init__(self):
        self.memory = None

    def SetMemory(self, memory):
        self.memory = memory

    def Step(self, trace, action):
        if trace._opCode == 2:
            self.memory.WriteTrace(trace, action)
        