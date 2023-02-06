from ..environment.trace import Trace
from ..model.networks import ValueNetworks, ActionSpace
from ..model.inference import InferenceLoader
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from collections import namedtuple
import csv

Record = namedtuple('Record', ['op_code', 'fid', 'lba', 'num_bytes', 'action', 'reward'])

class History:
    def __init__(self):
        self.records = [] 
    
    def Add(self, trace, action, reward):
        opcode = trace._opCode
        fid = trace._fid
        lba = trace._lba
        num_bytes = trace._bytes
        if action == None:
            type = 'None'
        else:
            type = 'hot' if action else 'cold'
        self.records.append(Record(opcode, fid, lba, num_bytes, type, reward))
    
    def WriteHistory(self, path):
        with open(path, 'w', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(self.records)

    def __len__(self):
        return len(self.records)

class ValidationLoader:
    def __init__(self):
        # Validation on
        self._inferenceLoader = InferenceLoader()
        self._inferenceLoader.Load()
        self._valueNetworks = ValueNetworks()
        self._valueNetworks.SetActionSpace(ActionSpace())
        self.episodes = []
        self.accs = []
        self.pres = []
        self.recalls = []
        self.F1s = []

    def ResetAll(self):
        self._inferenceLoader.Reset()
        self.episodes.clear()
        self.accs.clear()
        self.pres.clear()
        self.recalls.clear()
        self.F1s.clear()

    def ConfusionMatrix(self, episode, yTrue, yPred):
        confusionMatrix = confusion_matrix(yTrue, yPred) 
        tn, fp, fn, tp = confusionMatrix.ravel()
        acc = (tp+tn)/(tp+fp+fn+tn)
        pre = tp/(tp+fp)
        recall = tp/(tp+fn)
        F1 = 2 / ((1/ pre) + (1/ recall))
        self.episodes.append(episode)
        self.accs.append(acc)
        self.pres.append(pre)
        self.recalls.append(recall)
        self.F1s.append(F1)
    
    def WriteHistory(self, path):
        with open(path, 'w') as file:
            for i in range(len(self.episodes)):
                file.write(f'{self.episodes[i]},{self.accs[i]},{self.pres[i]},{self.recalls[i]},{self.F1s[i]}\n')

    def DrawHistory(self, path):
        plt.plot(self.episodes, self.accs, label="acc")
        plt.plot(self.episodes, self.pres, label="pre")
        plt.plot(self.episodes, self.recalls, label="recall")
        plt.plot(self.episodes, self.F1s, label="F1")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.title("Validation")
        plt.xlim(left = self.episodes[0] - 5)
        plt.legend()
        plt.savefig(path)
        plt.clf()

    def Validation(self, episode, valueNetworks):
        self._valueNetworks = valueNetworks
        yTarget = self._inferenceLoader._Y
        xTarget = self._inferenceLoader._X
        yPred = []
        for i in range(len(yTarget)):
            yPred.append(self._valueNetworks.GetModelAction(xTarget[i], 0))
        self.ConfusionMatrix(episode, yTarget, yPred)