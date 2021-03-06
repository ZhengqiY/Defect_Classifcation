# -*- coding: utf-8 -*-
"""Homework2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19gVExZgyw-9WbhHhMbOoiensUHSaJKm3
"""

from google.colab import drive
drive.mount('/content/drive')

import numpy as np
from google.colab import files
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from keras.models import Sequential
from keras.layers import Input, Dense, Activation, Conv2D, MaxPooling2D, Dropout, Flatten, BatchNormalization
from keras import optimizers
from keras import losses
from keras.callbacks import ModelCheckpoint
from keras.preprocessing.image import ImageDataGenerator
from matplotlib import pyplot

uploaded = files.upload()

# load dataset
train_x = np.load('train_data.npy')
train_x = train_x.reshape(400,64,64,1)
train_y = np.load('train_label.npy')

# Preprocessing Training label set Y


def prepare_labels(labels):
    ohe = OneHotEncoder()
    # reshape labels to be 2D array
    labels = labels.reshape(len(labels),1)
    ohe.fit(labels)
    labels_enc = ohe.transform(labels).toarray()
    return labels_enc


y_processed = prepare_labels(train_y)

# Split Training set and validation set

x_train, x_vali, y_train, y_true = train_test_split(train_x,  \
                                y_processed, test_size = 0.3)

# create image data augmentation generator
datagen = ImageDataGenerator(shear_range=1)
#datagen.fit(x_train)

pyplot.imshow(x_train[11].reshape(64, 64), cmap=pyplot.get_cmap('gray'))

for X_batch, y_batch in datagen.flow(x_train, y_train, batch_size=9):
	# create a grid of 3x3 images
	for i in range(0, 9):
		pyplot.subplot(330 + 1 + i)
		pyplot.imshow(X_batch[i].reshape(64, 64), cmap=pyplot.get_cmap('gray'))
	# show the plot
	pyplot.show()
	break

# Model

model = Sequential()

model.add(Conv2D(16,(3,3), input_shape=(64,64,1), strides=(1,1), padding='same', activation='relu',
                 use_bias=True, kernel_initializer='RandomNormal', bias_initializer='RandomNormal'))
model.add(MaxPooling2D(pool_size=(2,2), strides=None))
model.add(Dropout(0.25))

model.add(Conv2D(32,(3,3), strides=(1,1), padding='same', activation='relu',
                 use_bias=True, kernel_initializer='RandomNormal', bias_initializer='RandomNormal'))
model.add(MaxPooling2D(pool_size=(2,2), strides=None))
model.add(Dropout(0.25))

model.add(Conv2D(64,(3,3), strides=(1,1), padding='same', activation='relu',
                 use_bias=True, kernel_initializer='RandomNormal', bias_initializer='RandomNormal'))
model.add(MaxPooling2D(pool_size=(2,2), strides=None))
model.add(Dropout(0.25))

#model.add(Conv2D(64,(3,3), strides=(1,1), padding='same', activation='relu',
#          use_bias=True, kernel_initializer='RandomNormal', bias_initializer='RandomNormal'))
#model.add(MaxPooling2D(pool_size=(2,2), strides=None))
#model.add(Dropout(0.25))
#model.add(Conv2D(256,(3,3), strides=(1,1), padding='same', activation='relu'))
#model.add(MaxPooling2D(pool_size=(2,2), strides=None))
#model.add(Dropout(0.5))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(6, activation='softmax'))


# Training and validating

model.compile('rmsprop', 'categorical_crossentropy', metrics=['accuracy'],)
filepath = "weights-improvement-{epoch:02d}-{val_accuracy:.2f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_loss',verbose=1,save_best_only=True, mode='max')
callbacks_list = [checkpoint]
model.fit_generator(datagen.flow(x_train, y_train, batch_size=10), steps_per_epoch=len(x_train)/10,
          epochs=150, verbose=1, validation_data=(x_vali,y_true))

# Confusion Matrix

y_pred = model.predict(x_vali)
y_pred_cm = y_pred.argmax(axis=1)
y_true_cm = y_true.argmax(axis=1)
confusion_matrix(y_true_cm, y_pred_cm)

# Classification Report
target_names = list(np.unique(train_y))
print(classification_report(y_true_cm, y_pred_cm, target_names=target_names))

model.save_weights('b9425_try.h5')

test_x = np.load('test_data.npy')
test_x = test_x.reshape(400,64,64,1)
res = model.predict(test_x)
res = res.argmax(axis=1)
#print(res)
#res_cm = res_cm.reshape(400,1)
#np.save('prediction', res)

res_str = []

for num in res:
  if num == 4:
    num = 'pass'
  elif num == 3:
    num = 'nodule'
  elif num == 2:
    num = 'edge'
  elif num == 0:
    num = 'crack'
  elif num == 1:
    num = 'deform'
  elif num == 5:
    num = 'total_loss'
  res_str.append(num)

np.save('prediction', res_str)
print(res_str)