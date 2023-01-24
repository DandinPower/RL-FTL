import tensorflow as tf
import numpy as np
from .q_model import QModel
from ..environment.environment import ActionSpace
from dotenv import load_dotenv
import os
load_dotenv()

WEIGHT_PATH = os.getenv('WEIGHT_PATH')

PARAMETER_NUMS = int(os.getenv('PARAMETER_NUMS'))
HIDDEN_SIZE = int(os.getenv('HIDDEN_SIZE'))
ACTION_NUMS = int(os.getenv('ACTION_NUMS'))

LR = float(os.getenv('LR'))
GAMMA = float(os.getenv('GAMMA'))

RNG = np.random.default_rng(100)

class ValueNetworks:
    def __init__(self):
        self._net = QModel(PARAMETER_NUMS, HIDDEN_SIZE, ACTION_NUMS)
        self._targetNet = QModel(PARAMETER_NUMS, HIDDEN_SIZE, ACTION_NUMS)
        self._optimizer = tf.keras.optimizers.Adam(learning_rate = LR) 
        self._loss = tf.keras.losses.Huber()

    def UpdateTargetNetwork(self):
        self._targetNet(np.array([[0.0, 0.0, 0.0]]))
        self._net(np.array([[0.0, 0.0, 0.0]]))
        self._targetNet.set_weights(self._net.get_weights())

    def UpdateOptimizerLR(self, lr):
         self._optimizer.learning_rate.assign(lr)

    def Optimize(self, batchData):
        states = np.array([d[0] for d in batchData], dtype=np.float32)
        actions = np.array([d[1] for d in batchData])
        rewards = np.array([d[2] for d in batchData])
        next_states = np.array([d[3] for d in batchData], dtype=np.float32)
        with tf.GradientTape() as tape:
            model_output = self._net(states)
            target_output = self._targetNet(next_states)
            model_output = tf.gather_nd(model_output, tf.expand_dims(actions, 1), 1)
            next_state_values = tf.math.reduce_max(target_output, axis = 1)
            expected_q_values = (next_state_values * GAMMA) + rewards
            loss = self._loss(expected_q_values, model_output)
            grads = tape.gradient(loss, self._net.variables)
            self._optimizer.apply_gradients(grads_and_vars=zip(grads, self._net.variables))

    def SetActionSpace(self, actionSpace: ActionSpace):
        self._actionSpace = actionSpace 

    #跟據state, epsilon以及給定的model來決定action
    def GetModelAction(self, state, epsilon):
        if RNG.uniform() < epsilon:
            return self._actionSpace.Sample()
        else:
            q_values = self._net(np.array([state],dtype = np.float32))
            return np.argmax(q_values) == 1
        
    # 儲存q model參數
    def SaveWeight(self):
        self._net.save_weights(WEIGHT_PATH)

    # 讀取參數
    def LoadWeight(self):
        self._net(np.zeros((1, PARAMETER_NUMS), dtype = np.float32))
        self._net.load_weights(WEIGHT_PATH)