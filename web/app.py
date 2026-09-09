from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
import io
from pathlib import Path

app = Flask(__name__)

# ==============================
# PATH MODEL
# ==============================

ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "models" / "cat_dog_mobilenetv2.keras"

print("Đang load model...")
print("Model:", MODEL_PATH)

model = tf.keras.models.load_model(MODEL_PATH)

print("Load model thành công!")

# ==============================
# CONFIG
# ==============================

IMG_SIZE = (224, 224)


# ==============================
# HOME
# ==============================

@app.route("/")
def home():
    return render_template("index.html")

# ==============================
# PREDICT API
# ==============================

@app.route("/predict", methods=["POST"])
def predict():

    # Kiểm tra có file ảnh hay không
    if "image" not in request.files:
        return jsonify({
            "error": "Không tìm thấy ảnh"
        }), 400

    file = request.files["image"]

    # Kiểm tra tên file
    if file.filename == "":
        return jsonify({
            "error": "Chưa chọn ảnh"
        }), 400

    try:

        # ==============================
        # ĐỌC ẢNH
        # ==============================

        image = tf.keras.utils.load_img(
            io.BytesIO(file.read()),
            target_size=IMG_SIZE
        )

        # Chuyển ảnh thành array
        image_array = tf.keras.utils.img_to_array(image)

        # Thêm batch dimension
        image_array = np.expand_dims(
            image_array,
            axis=0
        )

        # ==============================
        # PREDICT
        # ==============================

        # KHÔNG preprocess ở đây
        # Vì model đã có preprocess_input bên trong

        prediction = model.predict(
            image_array,
            verbose=0
        )[0][0]

        # ==============================
        # CLASSIFICATION
        # ==============================

        if prediction >= 0.5:

            label = "DOG"
            confidence = prediction

        else:

            label = "CAT"
            confidence = 1 - prediction

        # ==============================
        # RETURN RESULT
        # ==============================

        return jsonify({

            "prediction": label,

            "confidence": round(
                float(confidence) * 100,
                2
            ),

            "raw_prediction": round(
                float(prediction),
                4
            )

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==============================
# RUN SERVER
# ==============================

import os

if __name__ == "__main__":
    app.run(
        debug=False,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )