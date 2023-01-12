from ..environment.environment import Environment
from ..libs.history import History
from dotenv import load_dotenv
from tqdm import tqdm
import random
import os
load_dotenv()

EPISODES = int(os.getenv('EPISODES'))
MAX_STEP = int(os.getenv('MAX_STEP'))

class Agent:
    def __init__(self):
        self._environment = Environment()
        self._history = History()

    def Train(self):
        for i in tqdm(range(EPISODES)):
            state = self._environment.ResetEpisode()
            for j in range(MAX_STEP):
                action = self.GetAction(state)
                reward, nextState = self._environment.Step(action)
                self._history.Add(state.trace, action, reward)
                state = nextState
        self._history.WriteHistory('python/history/record.csv')

    # True為Hot, False為Cold
    def GetAction(self, trace):
        return random.choice(self._environment._sampleSpace)