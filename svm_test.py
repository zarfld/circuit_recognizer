import os
import sys
import cv2
import numpy as np
from tensorflow.keras.models import load_model

def get_hog():
    winSize = (100, 100)
    blockSize = (10, 10)
    blockStride = (5, 5)
    cellSize = (10, 10)
    nbins = 9
    derivAperture = 1
    winSigma = -1.0
    histogramNormType = 0
    L2HysThreshold = 0.2
    gammaCorrection = 1
    nlevels = 64
    signedGradient = True

    hog = cv2.HOGDescriptor(
        winSize,
        blockSize,
        blockStride,
        cellSize,
        nbins,
        derivAperture,
        winSigma,
        histogramNormType,
        L2HysThreshold,
        gammaCorrection,
        nlevels,
        signedGradient,
    )

    return hog

def load_trainData(image_path):
    trainData = []
    trainLabel = []
    i = 0
    for path in sorted(os.listdir(image_path)):

        files = os.listdir(image_path + '/' + path)
        for f in files:
            if f.endswith('.png') or f.endswith('.jpeg') or f.endswith('.jpg'):
                trainData.append(image_path + '/' + path + '/' + f)
                trainLabel.extend([x for x in np.repeat(i, 4)])

        print("{} -> {} ".format(path, i))
        i = i + 1

    return trainData, trainLabel

def augment_image(image):
    augmented_images = []
    rows, cols = image.shape

    # Original image
    augmented_images.append(image)

    # Rotations
    for angle in [90, 180, 270]:
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
        dst = cv2.warpAffine(image, M, (cols, rows))
        augmented_images.append(dst)

    # Flipping
    augmented_images.append(cv2.flip(image, 0))  # Vertical flip
    augmented_images.append(cv2.flip(image, 1))  # Horizontal flip
    augmented_images.append(cv2.flip(image, -1))  # Both axes flip

    return augmented_images

def interpret_color_code(resistor_image):
    resistor_image = cv2.cvtColor(resistor_image, cv2.COLOR_BGR2RGB)
    resistor_image = cv2.resize(resistor_image, (200, 50))
    bands = segment_color_bands(resistor_image)
    colors = [color.rgb2lab(band) for band in bands]
    color_codes = {
        "black": (0, 0, 0),
        "brown": (1, 10, 1, 100),
        "red": (2, 100, 2, 50),
        "orange": (3, 1000, None, 15),
        "yellow": (4, 10000, None, 25),
        "green": (5, 100000, 0.5, None),
        "blue": (6, 1000000, 0.25, None),
        "violet": (7, 10000000, 0.1, None),
        "grey": (8, None, 0.05, None),
        "white": (9, None, None, None),
        "gold": (None, 0.1, 5, None),
        "silver": (None, 0.01, 10, None)
    }
    band_values = []
    for color_lab in colors:
        min_distance = float('inf')
        closest_color = None
        for color_name, color_value in color_codes.items():
            distance = np.linalg.norm(color_lab - color.rgb2lab(np.uint8([[color_value[:3]]])))
            if distance < min_distance:
                min_distance = distance
                closest_color = color_name
        band_values.append(color_codes[closest_color])
    if len(band_values) == 4:
        resistance = (band_values[0][0] * 10 + band_values[1][0]) * band_values[2][1]
        tolerance = band_values[3][2]
        temp_coeff = None
    elif len(band_values) == 5:
        resistance = (band_values[0][0] * 100 + band_values[1][0] * 10 + band_values[2][0]) * band_values[3][1]
        tolerance = band_values[4][2]
        temp_coeff = None
    elif len(band_values) == 6:
        resistance = (band_values[0][0] * 100 + band_values[1][0] * 10 + band_values[2][0]) * band_values[3][1]
        tolerance = band_values[4][2]
        temp_coeff = band_values[5][3]
    return resistance, tolerance, temp_coeff

if __name__ == '__main__':

    image_path = "data/test"
    testData, testLabel = load_trainData(image_path)

    # HoG feature descriptor
    hog = get_hog()
    hog_descriptors = []
    svm = cv2.ml.SVM_load("svm_data.dat")
    cnn_model = load_model("cnn_model.h5")

    k = 0
    for data in testData:
        img = cv2.imread(data, 0)
        resized_img = cv2.resize(img, (100, 100), interpolation=cv2.INTER_CUBIC)
        gauss_img = cv2.GaussianBlur(resized_img, (9, 9), 0)
        th = cv2.adaptiveThreshold(
            gauss_img,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11,
            2,
        )

        augmented_images = augment_image(th)
        for aug_img in augmented_images:
            hog_descriptors.append(hog.compute(aug_img))

        k = k + 1

    truePos = [0, 0, 0]
    predictedPos = [0, 0, 0]
    total = len(testLabel)
    for (hog_des, label, i) in zip(hog_descriptors, testLabel, range(1, total + 1)):
        _, result = svm.predict(np.array(hog_des, np.float32).reshape(-1, 3249))
        idx = int(result[0][0])
        if idx == label:
            truePos[label] = truePos[label] + 1

        predictedPos[idx] = predictedPos[idx] + 1

    for i in range(len(truePos)):
        precision = truePos[i] / float(predictedPos[i])
        recall = truePos[i] / float((total / 3))
        print("{} \nprecision :{:.3f}\trecall :{:.3f}".format(i, precision, recall))
        print("{}\t{}".format(truePos[i], total / 3))

    # CNN model testing
    test_images = []
    for data in testData:
        img = cv2.imread(data, 0)
        resized_img = cv2.resize(img, (100, 100), interpolation=cv2.INTER_CUBIC)
        test_images.append(resized_img)
    test_images = np.array(test_images).reshape(-1, 100, 100, 1)

    cnn_predictions = cnn_model.predict(test_images)
    cnn_predicted_labels = np.argmax(cnn_predictions, axis=1)

    cnn_truePos = [0, 0, 0]
    cnn_predictedPos = [0, 0, 0]
    for label, pred_label in zip(testLabel, cnn_predicted_labels):
        if pred_label == label:
            cnn_truePos[label] = cnn_truePos[label] + 1

        cnn_predictedPos[pred_label] = cnn_predictedPos[pred_label] + 1

    for i in range(len(cnn_truePos)):
        precision = cnn_truePos[i] / float(cnn_predictedPos[i])
        recall = cnn_truePos[i] / float((total / 3))
        print("CNN {} \nprecision :{:.3f}\trecall :{:.3f}".format(i, precision, recall))
        print("CNN {}\t{}".format(cnn_truePos[i], total / 3))

    # Resistor color code detection testing
    resistor_test_images = [cv2.imread(data, 1) for data in testData if "resistor" in data]
    for resistor_image in resistor_test_images:
        resistance, tolerance, temp_coeff = interpret_color_code(resistor_image)
        print(f"Resistor: {resistance}Ω ±{tolerance}% {temp_coeff}ppm/°C" if temp_coeff else f"Resistor: {resistance}Ω ±{tolerance}%")
