import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json
import os

def load_data():
    # Load and preprocess your data
    train_data_gen = ImageDataGenerator(rescale=1./255).flow_from_directory('dataset/train/', target_size=(150, 150))
    val_data_gen = ImageDataGenerator(rescale=1./255).flow_from_directory('dataset/val/', target_size=(150, 150))
    return train_data_gen, val_data_gen

def build_model():
    model = Sequential([
        Conv2D(32, (3,3), activation='relu', input_shape=(150, 150, 3)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def preprocess_annotations(data_dir):
    annotations = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            with open(os.path.join(data_dir, filename), 'r') as file:
                data = json.load(file)
                for component in data.get('components', []):
                    annotations.append({
                        'componentType': component.get('componentType', ''),
                        'partNumber': component.get('partNumber', ''),
                        'value': component.get('value', ''),
                        'boundingBox': component.get('boundingBox', {})
                    })
    return annotations

def train_model():
    train_data, val_data = load_data()
    model = build_model()
    model.fit(train_data, epochs=10, validation_data=val_data)
    model.save('saved_model/my_model')

if __name__ == '__main__':
    train_model()
