import os
import numpy as np
import tensorflow as tf
from PIL import Image
from flask import Flask, render_template, request
from keras.preprocessing.image import load_img, img_to_array

# Initialize Flask app
app = Flask(name)

# Load the trained model
model = tf.keras.models.load_model("model.h5")

# Home page route
@app.route('/')
def index():
    return render_template("index.html")

# Prediction route
@app.route('/predict', methods=['GET', 'POST'])
def output():
    if request.method == 'POST':
        f = request.files['pc_image']
        
        # Save the uploaded image to static/uploads/
        upload_folder = "static/uploads/"
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        img_path = os.path.join(upload_folder, f.filename)
        f.save(img_path)

        # Load and preprocess the image
        img = load_img(img_path, target_size=(224, 224))
        image_array = img_to_array(img) / 255.0  # Normalize
        image_array = np.expand_dims(image_array, axis=0)

        # Predict
        pred = model.predict(image_array)
        pred_class = np.argmax(pred, axis=1)[0]

        # Map prediction index to labels
        classes = ['Coccidiosis', 'Healthy', 'New Castle Disease', 'Salmonella']
        prediction = classes[pred_class]

        return render_template('contact.html', predict=prediction)

    return render_template('contact.html', predict="No file uploaded.")
    
# Run the app
if name == 'main':
    app.run(debug=True)
