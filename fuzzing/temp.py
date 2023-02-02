import tensorflow as tf
import os
import numpy as np
from tensorflow.python.ops import nn_impl
try:
  arg_0_tensor = tf.saturate_cast(tf.random.uniform([3, 3, 3], minval=0, maxval=2, dtype=tf.int64), dtype=tf.uint64)
  arg_0 = tf.identity(arg_0_tensor)
  arg_1_tensor = tf.cast(tf.random.uniform([3, 3, 3], minval=0, maxval=2, dtype=tf.int32), dtype=tf.bool)
  arg_1 = tf.identity(arg_1_tensor)
  arg_2 = -14
  arg_3 = True
  out = nn_impl.weighted_cross_entropy_with_logits_v2(arg_0,arg_1,arg_2,arg_3,)
except Exception as e:
  print("Error:"+str(e))