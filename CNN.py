# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1s2GiMPRE7egL7s5JfHQ5QjWjTgsxZSFp
"""

!rm -rf Dataset

from google.colab import drive
drive.mount('/content/drive2')

!unzip -q "/content/drive2/My Drive/Dataset.zip"

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.image as mpimg

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import logging
logger = tf.get_logger()
logger.setLevel(logging.ERROR)

base_dir = os.path.join( 'Dataset')
train_dir = os.path.join(base_dir, 'Train')
validation_dir = os.path.join(base_dir, 'validation')
test_dir=os.path.join(base_dir,'test')
train_animals_dir = os.path.join(train_dir, 'animals')
train_humans_dir = os.path.join(train_dir, 'human')
validation_animals_dir = os.path.join(validation_dir, 'animals')
validation_humans_dir = os.path.join(validation_dir, 'human')
tests_animals_dir = os.path.join(test_dir, 'animals')
tests_humans_dir = os.path.join(test_dir, 'human')

num_animals_tr = len(os.listdir(train_animals_dir))
num_humans_tr=len(os.listdir(train_humans_dir))
num_animals_val = len(os.listdir(validation_animals_dir))
num_humans_val=len(os.listdir(validation_humans_dir))
num_animals_ts = len(os.listdir(tests_animals_dir))
num_humans_ts=len(os.listdir(tests_humans_dir))

total_train = num_animals_tr+num_humans_tr
total_val = num_animals_val+num_humans_val
total_test=num_animals_ts+num_humans_ts

print('Животных в тестовом наборе данных: ', num_animals_tr)
print('Людей в тестовом наборе данных: ', num_humans_tr)
print('Животных в валидационном наборе данных: ', num_animals_val)
print('Людей в валидационном наборе данных: ', num_humans_val)
print('--')
print('Всего изображений в тренировочном наборе данных: ', total_train)
print('Всего изображений в валидационном наборе данных: ', total_val)
print('Всего изображений в тестовом наборе данных: ', total_test)

BATCH_SIZE = 100 # количество тренировочных изображений для обработки перед обновлением параметров модели
IMG_SHAPE = 150 # размерность к которой будет преведено входное изображение

def plotImages(images_arr):
  fig, axes = plt.subplots(1, 5, figsize=(20,20))
  axes = axes.flatten()
  for img, ax in zip(images_arr, axes):
    ax.imshow(img)
  plt.tight_layout()
  plt.show()

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(IMG_SHAPE, IMG_SHAPE, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(2, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

image_gen = ImageDataGenerator(rescale=1./255, horizontal_flip=True)

train_data_gen = image_gen.flow_from_directory(batch_size=BATCH_SIZE,
                                               directory=train_dir,
                                               shuffle=True,
                                               target_size=(IMG_SHAPE, IMG_SHAPE))

image_gen = ImageDataGenerator(rescale=1./255, rotation_range=45)

train_data_gen = image_gen.flow_from_directory(batch_size=BATCH_SIZE,
                                               directory=train_dir,
                                               shuffle=True,
                                               target_size=(IMG_SHAPE, IMG_SHAPE))

image_gen = ImageDataGenerator(rescale=1./255, zoom_range=0.5)

train_data_gen = image_gen.flow_from_directory(batch_size=BATCH_SIZE,
                                               directory=train_dir,
                                               shuffle=True,
                                               target_size=(IMG_SHAPE, IMG_SHAPE))

image_gen_train = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

train_data_gen = image_gen_train.flow_from_directory(batch_size=BATCH_SIZE,
                                                     directory=train_dir,
                                                     shuffle=True,
                                                     target_size=(IMG_SHAPE, IMG_SHAPE),
                                                     class_mode='binary')

image_gen_val = ImageDataGenerator(rescale=1./255)

val_data_gen = image_gen_val.flow_from_directory(batch_size=BATCH_SIZE,
                                                 directory=validation_dir,
                                                 target_size=(IMG_SHAPE, IMG_SHAPE),
                                                 class_mode='binary')

image_gen_test=ImageDataGenerator(rescale=1./255)

test_data_gen = image_gen_test.flow_from_directory(batch_size=BATCH_SIZE,
                                                 directory=test_dir,
                                                 target_size=(IMG_SHAPE, IMG_SHAPE),
                                                 class_mode='binary')

EPOCHS = 250
history = model.fit_generator(
    train_data_gen,
    steps_per_epoch=int(np.ceil(total_train / float(BATCH_SIZE))),
    epochs=EPOCHS,
    validation_data=val_data_gen,
    validation_steps=int(np.ceil(total_val / float(BATCH_SIZE)))
)

model.save_weights("model.h5")

model.load_weights('model.h5')

test_loss, test_accuracy = model.evaluate(test_data_gen, steps=math.ceil(total_test))
print("Точность на тестовом наборе данных: ", test_accuracy)

TEST_FILE = "test_file.txt"
open(TEST_FILE,"w")
probabilities = model.predict_generator(test_data_gen, 374)
for index, probability in enumerate(probabilities):
    image_path = test_dir + "/" +test_generator.filenames[index]
    img = mpimg.imread(image_path)
    with open(TEST_FILE,"a") as fh:
        fh.write(str(probability[0]) + " for: " + image_path + "\n")
    plt.imshow(img)
    if probability > 0.5:
        plt.title("%.2f" % (probability[0]*100) + "% human")
    else:
        plt.title("%.2f" % ((1-probability[0])*100) + "% animal")
    plt.show()