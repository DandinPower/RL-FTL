import tensorflow as tf 
import numpy as np
import random 
from dotenv import load_dotenv
import os
load_dotenv()

FID_FREQUENCY_SAMPLE_RANGE = int(os.getenv('FID_FREQUENCY_SAMPLE_RANGE'))
LBA_DIFF_SAMPLE_RANGE = int(os.getenv('LBA_DIFF_SAMPLE_RANGE'))
NUM_BYTES_SAMPLE_RANGE = int(os.getenv('NUM_BYTES_SAMPLE_RANGE'))
NUM_BYTES_BIGGER_THAN_LBA_RANGE = int(os.getenv('NUM_BYTES_BIGGER_THAN_LBA_RANGE'))

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
        x = self.layer1(inputs)
        x = self.relu(x)
        x = self.layer2(x)
        x = self.relu(x)
        x = self.action(x)
        x = tf.squeeze(x)
        return x
    
class QEmbeddingModel(tf.keras.Model):
    def __init__(self, _embeddSize, _hiddenSize, _actionNums):
        super(QEmbeddingModel, self).__init__()
        self.embedding_fid_freq = tf.keras.layers.Embedding(FID_FREQUENCY_SAMPLE_RANGE, _embeddSize)
        self.embedding_lba_diff = tf.keras.layers.Embedding(LBA_DIFF_SAMPLE_RANGE, _embeddSize)
        self.embedding_bytes = tf.keras.layers.Embedding(NUM_BYTES_SAMPLE_RANGE, _embeddSize)
        self.embedding_bytes_bigger_than_lba = tf.keras.layers.Embedding(NUM_BYTES_BIGGER_THAN_LBA_RANGE, _embeddSize)
        self.layer1 = LinearLayer(_embeddSize, _hiddenSize)
        self.layer2 = LinearLayer(_hiddenSize, _hiddenSize)
        self.action = LinearLayer(_hiddenSize, _actionNums)
        self.relu = tf.keras.layers.ReLU()

    def call(self, inputs):
        fid_freq = tf.slice(inputs, [0, 0], [-1, 1])
        lba_diff = tf.slice(inputs, [0, 1], [-1, 1])
        bytes = tf.slice(inputs, [0, 2], [-1, 1])
        bytes_bigger_than_lba = tf.slice(inputs, [0, 3], [-1, 1])
        embedded_inputs = self.embedding_fid_freq(fid_freq) + self.embedding_lba_diff(lba_diff) + self.embedding_bytes(bytes) + self.embedding_bytes_bigger_than_lba(bytes_bigger_than_lba)
        x = self.layer1(embedded_inputs)
        x = self.relu(x)
        x = self.layer2(x)
        x = self.relu(x)
        x = self.action(x)
        x = tf.squeeze(x)
        return x