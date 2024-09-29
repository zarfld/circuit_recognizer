import os
import sys
import cv2
import numpy as np
from sklearn.utils import shuffle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical

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
        files = os.listdir(image_path + "/" + path)
        for f in files:
            if f.endswith(".png") or f.endswith(".jpeg") or f.endswith(".jpg"):
                trainData.append(image_path + "/" + path + "/" + f)
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

def create_cnn_model(input_shape, num_classes):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

if __name__ == "__main__":
    image_path = "data/train"
    trainData, trainLabel = load_trainData(image_path)

    # HoG feature descriptor
    hog = get_hog()
    hog_descriptors = []
    augmented_labels = []
    svm = cv2.ml.SVM_create()
    svm.setKernel(cv2.ml.SVM_RBF)
    svm.setType(cv2.ml.SVM_C_SVC)

    k = 0
    for data, label in zip(trainData, trainLabel):
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
        cv2.imwrite("data/th/" + str(k) + ".jpg", th)

        augmented_images = augment_image(th)
        for aug_img in augmented_images:
            hog_descriptors.append(hog.compute(aug_img))
            augmented_labels.append(label)

        k = k + 1

    hog_descriptors, augmented_labels = shuffle(hog_descriptors, augmented_labels)

    svm.trainAuto(
        np.array(hog_descriptors, np.float32),
        cv2.ml.ROW_SAMPLE,
        np.array(augmented_labels),
    )
    svm.save("svm_data.dat")

    # CNN model training
    input_shape = (100, 100, 1)
    num_classes = len(set(trainLabel))
    cnn_model = create_cnn_model(input_shape, num_classes)

    # Prepare data for CNN
    train_images = []
    for data in trainData:
        img = cv2.imread(data, 0)
        resized_img = cv2.resize(img, (100, 100), interpolation=cv2.INTER_CUBIC)
        train_images.append(resized_img)
    train_images = np.array(train_images).reshape(-1, 100, 100, 1)
    train_labels = to_categorical(trainLabel, num_classes)

    cnn_model.fit(train_images, train_labels, epochs=10, batch_size=32)
    cnn_model.save("cnn_model.h5")

    test = cv2.imread("data/img.jpg", 0)
    test_hog = hog.compute(test)
    re = svm.predict(np.array(test_hog, np.float32).reshape(-1, 3249))
    print(re)
