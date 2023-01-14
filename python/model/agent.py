from ..environment.environment import Environment
from ..libs.history import History
from .buffer import ReplayBuffer
from .record import TrainHistory
from .networks import ValueNetworks
from .parameter import HyperParameter
from dotenv import load_dotenv
from tqdm import tqdm
import numpy as np
import os
load_dotenv()

EPISODES = int(os.getenv('EPISODES'))
MAX_STEP = int(os.getenv('MAX_STEP'))
WARM_UP_EPISODES = int(os.getenv('WARM_UP_EPISODES'))
BATCH_SIZE = int(os.getenv('BATCH_SIZE'))
UPADTE_RATE = int(os.getenv('UPDATE_RATE'))

class Agent:
    def __init__(self):
        self._environment = Environment()
        self._history = History()
        self._buffer = ReplayBuffer()
        self._trainHistory = TrainHistory()
        self._hyperParameter = HyperParameter()
        self._valueNetworks = ValueNetworks()
        self._valueNetworks.SetActionSpace(self._environment._actionSpace)
        
    # 每一次的遊戲
    def Episode(self, episode):
        state = self._environment.ResetEpisode()
        rewardSum = 0
        for i in range(MAX_STEP):
            action = self._valueNetworks.GetModelAction(state, self._hyperParameter._epsilon)
            reward, nextState = self._environment.Step(action)
            rewardSum += reward 
            self._buffer.Add(state, action, reward, nextState)
            state = nextState
            if episode > WARM_UP_EPISODES:
                X = self._buffer.GetBatchData(BATCH_SIZE)
                self._valueNetworks.Optimize(X)
        self._trainHistory.AddHistory([episode, rewardSum, MAX_STEP, self._hyperParameter._epsilon])
        return rewardSum 

    # train 
    def Train(self):
        train_iter = tqdm(np.arange(EPISODES))
        for i in train_iter:
            rewardSum = self.Episode(i)
            self._hyperParameter.UpdateEpsilon(i)
            if i % UPADTE_RATE == 0:
                self._valueNetworks.UpdateTargetNetwork()
            if i > WARM_UP_EPISODES:
                self._hyperParameter.UpdateLearningRate(i - WARM_UP_EPISODES + 1)
                self._valueNetworks.UpdateOptimizerLR(self._hyperParameter._lr)
            train_iter.set_postfix_str(f"reward_sum: {rewardSum}")
        self._trainHistory.ShowHistory('python/history/q_version1.jpg')