from keras.models import load_model
from keras.preprocessing import image
import numpy as np
from tensorflow.keras.applications.inception_v3 import preprocess_input

def load_keras_model(model_file):
    model = load_model(model_file)
    return model
def prepare_image(file):
    img = image.load_img(file, target_size=(224, 224))  # Adjusted to match the model's expected input size
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return preprocess_input(img_array_expanded_dims)  # Use preprocess_input instead of just rescaling


def load_labels(labels_file):
    with open(labels_file, 'r') as f:
        labels = f.read().splitlines()
    return labels

def main(img):
    model_file = "new_food_recognition_model.h5"
    model = load_keras_model(model_file)
    prepared_image = prepare_image(img)
    predictions = model.predict(prepared_image)
    predicted_index = np.argmax(predictions)
    def your_mapping_function(predicted_index):
        food_categories = ['Chicken Briyani', 'Chicken Curry', 'Dosa', 'Fried Rice', 'Idly', 'Poori', 'Rice', 'Vada']
        if predicted_index < len(food_categories):
            return food_categories[predicted_index]
        else:
            return f"Label index {predicted_index} is out of range. Check your labels."

    # Get the matching score
    max_prediction_score = np.max(predictions)
    
    # Set your threshold for matching score
    if max_prediction_score > 0.90:
        result = your_mapping_function(predicted_index)
    elif 0.70 <= max_prediction_score <= 80:
        result = f"Possible match with {your_mapping_function(predicted_index)} (Matching Score: {max_prediction_score:.2f})"
    else:
        result = "Image cannot be recognized."

    return result