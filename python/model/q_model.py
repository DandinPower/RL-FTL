import tensorflow as tf 
import numpy as np
import random 

class LinearLayer(tf.keras.layers.Layer):
    def __init__(self, input_dim,output_dim):
        super().__init__()
        self.w = self.add_weight(name = "w",
            shape=[input_dim, output_dim], initializer="random_normal", trainable = True)
        self.b = self.add_weight(name = "b",
            shape=[output_dim], initializer="random_normal", trainable = True)

    def call(self, inputs):
        return tf.matmul(inputs, self.w) + self.b 

class QModel(tf.keras.Model):
    def __init__(self, _parameterNums, _hiddenSize, _actionNums):
        super(QModel, self).__init__()
        self.layer1 = LinearLayer(_parameterNums, _hiddenSize)
        self.layer2 = LinearLayer(_hiddenSize, _hiddenSize)
        self.action = LinearLayer(_hiddenSize, _actionNums)
        self.relu = tf.keras.layers.ReLU()
        
    def call(self, inputs):
        x = self.layer1(x)
        x = self.relu(x)
        x = self.layer2(x)
        x = self.relu(x)
        x = self.action(x)
        x = tf.squeeze(x)
        return x