from numpy import array
from os import path, listdir
from cv2 import IMREAD_GRAYSCALE, resize, imread
from tqdm import tqdm
from random import shuffle
from tensorflow import keras

# Constants
DATADIR = ["GC_SI"]
CATEGORIES = ["DOWN", "UP"]
IMG_SIZE = 256
training_data = []


def main():
    """
    Main function to prepare training data, create and train a CNN model, and evaluate its accuracy.
    """
    X, y = prepare_features_and_labels()

    train_images, test_images, train_labels, test_labels = split_data(X, y)

    model = create_model()

    model.fit(train_images, train_labels, epochs=2)

    test_loss, test_acc = model.evaluate(test_images, test_labels)
    print(f"\nTesting data provided loss: {test_loss} and accuracy: {test_acc}")


def prepare_features_and_labels():
    """
    Prepares the features (X) and labels (y) by loading and processing images.
    
    Returns:
        X (numpy.ndarray): Array of image data.
        y (list): Corresponding labels for the images.
    """
    create_training_data()
    shuffle(training_data)

    X = []
    y = []

    for features, label in training_data:
        X.append(features)
        y.append(label)

    X = array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    return X, y


def create_training_data():
    """
    Loads image data from directories and processes it into a standardized format.
    Images are resized and converted to grayscale.
    """
    for datadir in DATADIR:
        for category in CATEGORIES:
            category_path = path.join(datadir, category)
            class_label = CATEGORIES.index(category)
            for img_file in tqdm(listdir(category_path)):
                try:
                    img_array = imread(path.join(category_path, img_file), IMREAD_GRAYSCALE)
                    resized_image = resize(img_array, (IMG_SIZE, IMG_SIZE))
                    training_data.append([resized_image, class_label])
                except Exception as e:
                    print(f"Error processing image {img_file}: {str(e)}")


def split_data(X, y):
    """
    Splits the data into training and test sets.
    
    Args:
        X (numpy.ndarray): Array of image data.
        y (list): Corresponding labels for the images.
    
    Returns:
        tuple: Train and test images and labels.
    """
    train_images = array(X[100:] / 255.0)
    test_images = array(X[:100] / 255.0)
    train_labels = array(y[100:])
    test_labels = array(y[:100])
    
    return train_images, test_images, train_labels, test_labels


def create_model():
    """
    Creates a simple CNN model for image classification.
    
    Returns:
        keras.Sequential: The compiled Keras model.
    """
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(IMG_SIZE, IMG_SIZE)),
        keras.layers.Dense(1024, activation='relu'),
        keras.layers.Dense(2)
    ])

    model.compile(optimizer='adam',
                  loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])
    return model


if __name__ == '__main__':
    main()
