import numpy as np
import os
import cv2
from tqdm import tqdm
import random
import tensorflow as tf


DATADIR = [""]
CATEGORIES = ["DOWN", "UP"]

training_data = []
IMG_SIZE = 256


def create_training_data():
    for datadir in DATADIR:
        for category in CATEGORIES:

            path = os.path.join(datadir, category)
            class_num = CATEGORIES.index(category)

            for img in tqdm(os.listdir(path)):
                try:
                    img_array = cv2.imread(os.path.join(
                        path, img), cv2.IMREAD_GRAYSCALE)
                    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                    training_data.append([new_array, class_num])
                except Exception as e:
                    pass


def main():
    create_training_data()
    random.shuffle(training_data)

    X = []
    y = []

    for features, label in training_data:
        X.append(features)
        y.append(label)

    X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

    train_images = X[100:]
    test_images = X[:100]

    train_labels = y[100:]
    test_labels = y[:100]

    class_names = ["DOWN", "UP"]
    train_images = train_images / 255.0
    test_images = test_images / 255.0

    train_images = np.array(train_images)
    test_images = np.array(test_images)

    train_labels = np.array(train_labels)
    test_labels = np.array(test_labels)

    model = tf.keras.Sequential([tf.keras.layers.Flatten(input_shape=(
        IMG_SIZE, IMG_SIZE)), tf.keras.layers.Dense(1024, activation='relu'), tf.keras.layers.Dense(2)])
    model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(
        from_logits=True), metrics=['accuracy'])
    model.fit(train_images, train_labels, epochs=2)

    test_loss, test_acc = model.evaluate(test_images,  test_labels)
    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    predictions = probability_model.predict(test_images)

    print("\ntesting data provided loss: " +
          str(test_loss) + " and accuracy: " + str(test_acc))


if __name__ == '__main__':
    main()
