import os
import numpy as np  
import tensorflow as tf
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input

app = Flask(__name__)

model = load_model('model.h5')  

IMG_HEIGHT = 224
IMG_WIDTH = 224

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST': #verif daca fisierul este prezent în cererea POST
        file = request.files['file']
        if file:
            filepath = os.path.join('static', file.filename)
            file.save(filepath)

            #incarcare imagine + preprocesare
            img = tf.keras.preprocessing.image.load_img(filepath)
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            img_array = tf.image.resize_with_pad(img_array, 224, 224).numpy()            
            
            img_array = np.expand_dims(img_array, axis=0)  #dim pt batch size

            img_array = preprocess_input(img_array)

            #prezice utilizand modelul
            predictions = model.predict(img_array)
            class_idx = int(np.argmax(predictions, axis=1)[0])
            class_labels = {0: "Baby-Products", 1: "Beauty/Health", 2: "Clothing/Accesories", 3: "Electronics", 4: "Fruits/Vegetables", 5:"Grocery", 6: "Hobby/Arts/Stationery", 7: "Home/Kitchen/Tools", 8: "Pet Supplies", 9: "Sports/Outdoor" }
            predicted_label = class_labels.get(class_idx, "Unknown")

            #returneaza rez
            return jsonify({"predicted_class": predicted_label})
        return jsonify({"error": "No file uploaded"}), 400

if __name__ == '__main__':
    app.run(debug=True)


