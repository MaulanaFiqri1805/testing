from flask import Flask, jsonify,request, render_template
import os
from sklearn import model_selection
from werkzeug.utils import secure_filename
from tensorflow.keras.applications.imagenet_utils import preprocess_input
from tensorflow.keras.models import load_model, model_from_json
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from PIL import Image
import logging

app = Flask(__name__)


MODEL_ARCHITECTURE = 'model/clean721.json'
MODEL_WEIGHTS = 'model/clean721.h5'

PREDICTION_CLASSES = {
    0: ('Gambar Tidak Cocok', 'klasifikasi-noklasifikasi.html'),
    1: ('Tanaman Padimu Terkena', 'klasifikasi-bl.html'),
    2: ('Tanaman Padimu Terkena', 'klasifikasi-blb.html'),
    3: ('Tanaman Padimu Terkena', 'klasifikasi-bw.html'),
    4: ('Tanaman', 'klasifikasi-sh.html'),
}

# Fungsi untuk memuat model dari file
def load_model_from_file():
    try:
        with open(MODEL_ARCHITECTURE, 'r') as json_file:
            loaded_model_json = json_file.read()
        model = model_from_json(loaded_model_json)
        model.load_weights(MODEL_WEIGHTS)
        return model
    except Exception as e:
        logging.error(f"Error loading model: {str(e)}")
        return None

# Memuat model saat aplikasi dimulai
model = load_model_from_file()

# Fungsi untuk melakukan prediksi menggunakan model
def model_predict(img_path, model):
    try:
        TARGET_IMAGE_SIZE = (224, 224)
        test_image = load_img(img_path, target_size=TARGET_IMAGE_SIZE)
        logging.info("@@ Got Image for prediction")

        test_image = img_to_array(test_image) / 255
        test_image = np.expand_dims(test_image, axis=0)

        result = model.predict(test_image)
        pred_class = np.argmax(result, axis=1)[0]
        pred_prob = result[0][pred_class] * 100  # Convert to percentage

        return PREDICTION_CLASSES[pred_class][0], PREDICTION_CLASSES[pred_class][1], pred_prob
    except Exception as e:
        logging.error(f"Error predicting: {str(e)}")
        return 'Error', 'error.html', 0

# Routing untuk halaman utama
@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')

# Routing untuk halaman Blog
@app.route("/blog", methods=['GET'])
def blog():
    return render_template('blog.html')

# Routing untuk halaman Blog
@app.route("/contact", methods=['GET'])
def contact():
    return render_template('contact.html')

# Routing untuk halaman klasifikasi
@app.route("/klasifikasi", methods=['GET', 'POST'])
def klasifikasi():
    return render_template('klasifikasi.html')


# Routing untuk halaman prediksi
@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files['image']
        filename = secure_filename(file.filename)
        logging.info("@@ Input posted =", filename)

        file_path = os.path.join('static', 'user_uploaded', filename)
        file.save(file_path)

        logging.info("@@ Predicting class...")
        pred_class, output_page, pred_prob = model_predict(file_path, model)

        return render_template(output_page, pred_output=pred_class, pred_prob=pred_prob, user_image=file_path)


if __name__ == '__main__':
    app.run(debug=True)
