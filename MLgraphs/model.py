from numpy import array
from os import path, listdir
from cv2 import IMREAD_GRAYSCALE, resize, imread
from tqdm import tqdm
from random import shuffle
from tensorflow import keras


DATADIR = [""]
CATEGORIES = ["DOWN", "UP"]
training_data = []
IMG_SIZE = 256


def main():
    X = []
    y = []
    create_training_data()
    shuffle(training_data)
    for features, label in training_data:
        X.append(features)
        y.append(label)
    X = array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    train_images = array(X[100:] / 255.0)
    test_images = array(X[:100] / 255.0)
    train_labels = array(y[100:])
    test_labels = array(y[:100])
    model = keras.Sequential([keras.layers.Flatten(input_shape=(
        IMG_SIZE, IMG_SIZE)), keras.layers.Dense(1024, activation='relu'), keras.layers.Dense(2)])
    model.compile(optimizer='adam', loss=keras.losses.SparseCategoricalCrossentropy(
        from_logits=True), metrics=['accuracy'])
    model.fit(train_images, train_labels, epochs=2)
    test_loss, test_acc = model.evaluate(test_images,  test_labels)
    print("\ntesting data provided loss: " +
          str(test_loss) + " and accuracy: " + str(test_acc))


def create_training_data():
    for datadir in DATADIR:
        for category in CATEGORIES:
            newPath = path.join(datadir, category)
            class_num = CATEGORIES.index(category)
            for img in tqdm(listdir(newPath)):
                try:
                    img_array = imread(path.join(
                        path, img), IMREAD_GRAYSCALE)
                    new_array = resize(img_array, (IMG_SIZE, IMG_SIZE))
                    training_data.append([new_array, class_num])
                except Exception as e:
                    print(str(e))
                    pass


if __name__ == '__main__':
    main()
