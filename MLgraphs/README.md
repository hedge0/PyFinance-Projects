# Candlestick Direction Prediction Using TensorFlow

This program is designed to predict the direction (up or down) of the next candlestick in financial charts using image classification techniques. It leverages **TensorFlow** to train a neural network on labeled candlestick chart images and predicts whether the next candlestick will move **up** or **down**.

The program utilizes a dataset of candlestick images, split into **UP** and **DOWN** categories, and processes this data to build a model capable of predicting the future direction of candlesticks based on historical patterns.

## Features

- **Input**: 
  - A folder with two sub-folders: `UP` and `DOWN`, containing labeled candlestick images.
  - Each image represents a candlestick chart snapshot for either an upward or downward movement.
  
- **Output**:
  - A trained neural network model that predicts whether the next candlestick will be **UP** or **DOWN**.
  - The program outputs loss and accuracy metrics after training and testing the model.

- **TensorFlow Model**:
  - A convolutional neural network (CNN) built using **TensorFlow**.
  - The model is trained for binary classification between the two classes: UP and DOWN.

## Neural Network Architecture

The neural network architecture used for this project is simple yet effective for image classification:

- **Input Layer**: Flattened image data of size 256x256.
- **Hidden Layer**: Fully connected layer with 1024 neurons and ReLU activation.
- **Output Layer**: Dense layer with 2 neurons (one for each class: UP and DOWN).

## Setup and Installation

1. **Install Dependencies**:
    Ensure you have the following Python libraries installed:
    ```
    pip install numpy opencv-python tqdm tensorflow pandas yfinance
    ```

2. **Prepare Data**:
    - Create a directory named `GC_SI` with two sub-folders: `UP` and `DOWN`.
    - Place candlestick chart images into these respective sub-folders based on their direction.

3. **Run the Program**:
    - After preparing your dataset, you can run the program using:
    ```
    python model.py
    ```

## Usage

1. **Data Loading**:
   - The program loads and processes images from the `UP` and `DOWN` folders.
   - Images are resized to 256x256 and converted to grayscale for consistency.

2. **Model Training**:
   - The program splits the image data into training and testing sets.
   - It trains the TensorFlow model using a simple neural network architecture.

3. **Evaluation**:
   - After training, the program evaluates the model’s accuracy using the test set.
   - It prints the test loss and accuracy for you to assess the performance.

## Example

- Suppose you have a folder with candlestick chart images showing upward and downward movements.
- You place images indicating upward movements in the `UP` folder and downward movements in the `DOWN` folder.
- The program will train the neural network on these images and predict the direction of new, unseen candlestick charts.

## Considerations

- This program is meant for educational purposes and is a demonstration of image classification using TensorFlow.
- The quality of the model heavily depends on the quality and quantity of training data.
- Experimenting with different neural network architectures, more epochs, and larger datasets can improve accuracy.
