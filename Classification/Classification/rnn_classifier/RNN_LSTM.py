from __future__ import print_function

import tensorflow as tf
import random
import numpy as np
from audio_anaylsis import test_mfcc_list as mf
from rnn_classifier import net

#定义RNN(LSTM)网络
def dynamicRNN(net):
    #需要用到 类的

    # 输入x的形状： (batch_size, max_seq_len, n_input)
    # 输入seqlen的形状：(batch_size, )
    # 定义一个lstm_cell，隐层的大小为n_hidden（之前的参数）
    lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(net.n_hidden)

    # 使用tf.nn.dynamic_rnn展开时间维度
    # 此外sequence_length=seqlen也很重要，它告诉TensorFlow每一个序列应该运行多少步
    outputs, states = tf.nn.dynamic_rnn(lstm_cell, net.x, dtype=tf.float32,sequence_length=net.seqlen)
    
    # outputs的形状为(batch_size, max_seq_len, n_hidden)

    # 我们希望的是取出与序列长度相对应的输出。如一个序列长度为10，我们就应该取出第10个输出
    # 但是TensorFlow不支持直接对outputs进行索引，因此我们用下面的方法来做：

    net.batch_size = tf.shape(outputs)[0]
    # 得到每一个序列真正的index
    index = tf.range(0, net.batch_size) * net.seq_max_len + (net.seqlen - 1)
    outputs = tf.gather(tf.reshape(outputs, [-1, net.n_hidden]), index)

    # 给最后的输出
    return tf.matmul(outputs, net.weights['out']) + net.biases['out']

def train_RNN(net):  
    # 这里的pred是logits而不是概率
    pred = dynamicRNN(net)

    # 因为pred是logits，因此用tf.nn.softmax_cross_entropy_with_logits来定义损失
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=net.y))
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=net.learning_rate).minimize(cost)

    # 分类准确率
    correct_pred = tf.equal(tf.argmax(pred,1), tf.argmax(net.y,1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    #使用网络+优化
    optimizer,accuracy,cost=optimization(net)
    # 初始化
    init = tf.global_variables_initializer()

    # 训练
    with tf.Session() as sess:
        sess.run(init)
        step = 1
        while step * net.batch_size < net.training_iters:
            batch_x, batch_y, batch_seqlen = trainset                        #need continue #
            # 每run一次就会更新一次参数
            sess.run(optimizer, feed_dict={x: batch_x, y: batch_y, seqlen: batch_seqlen})
            if step % display_step == 0:
                # 在这个batch内计算准确度
                acc = sess.run(accuracy, feed_dict={x: batch_x, y: batch_y, seqlen: batch_seqlen})
                # 在这个batch内计算损失
                loss = sess.run(cost, feed_dict={x: batch_x, y: batch_y,seqlen: batch_seqlen})
                print("Iter " + str(step*net.batch_size) + ", Minibatch Loss= " + \
                      "{:.6f}".format(loss) + ", Training Accuracy= " + \
                      "{:.5f}".format(acc))
            step += 1
        print("Optimization Finished!")

        # 最终，我们在测试集上计算一次准确度
        test_data = testset.data
        test_label = testset.labels
        test_seqlen = testset.seqlen
        print("Testing Accuracy:", \
            sess.run(accuracy, feed_dict={x: test_data, y: test_label,seqlen: test_seqlen}))
        pass
