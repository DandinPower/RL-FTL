import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, RobustScaler
import numpy as np
import csv

class Graph:
    def __init__(self):
        self._x = []
        self._y = [] 
        #self.scaler = StandardScaler()
        self.scaler = RobustScaler()

    def ReadFromCsv(self, path):
        self._x.clear()
        self._y.clear()
        with open(path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self._x.append(int(row[0]))
                self._y.append(int(row[1]))
    
    def Draw(self, path):
        self._x = np.array([512, 4096, 8192, 10752, 16384])
        self._x = self._x.reshape(-1, 1)
        self._x = self.scaler.fit_transform(self._x)
        minInX = self._x.min()
        maxInX = self._x.max()
        newMin = 0
        newMax = 100
        self._x = self._x.flatten()
        self._x = list(map(lambda x: (x-minInX)/(maxInX-minInX) * (newMax - newMin) + newMin, self._x))
        
        #self.scaler.reset()
        self.scaler = RobustScaler()

        self._y = np.array([1, 1, 40, 1, 17])
        self._y = self._y.reshape(-1, 1)
        self._y = self.scaler.fit_transform(self._y)
        minInY = self._y.min()
        maxInY = self._y.max()
        newMin = 0
        newMax = 10
        self._y = self._y.flatten()
        self._y = list(map(lambda x: (x-minInY)/(maxInY-minInY) * (newMax - newMin) + newMin, self._y))
        print(self._y)
        plt.bar(self._x, self._y)
        #plt.semilogx()
        plt.semilogy()
        plt.savefig(path)