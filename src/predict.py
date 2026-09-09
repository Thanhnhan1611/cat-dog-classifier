import tensorflow as tf
import numpy as np
from pathlib import Path

# =========================
# CẤU HÌNH
# =========================

IMG_SIZE = (224, 224)

ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = ROOT / "models" / "cat_dog_mobilenetv2.keras"
IMAGE_PATH = ROOT / "test_image.jpg"

# =========================
# LOAD MODEL
# =========================

print("Đang load model...")

model = tf.keras.models.load_model(MODEL_PATH)

# =========================
# LOAD IMAGE
# =========================

print("Ảnh đang test:", IMAGE_PATH)

image = tf.keras.utils.load_img(
    IMAGE_PATH,
    target_size=IMG_SIZE
)

image_array = tf.keras.utils.img_to_array(image)

# Thêm batch dimension
image_array = np.expand_dims(image_array, axis=0)

# =========================
# PREDICT
# =========================

# KHÔNG preprocess ở đây!
# Vì model đã có preprocess_input bên trong.

prediction = model.predict(
    image_array,
    verbose=0
)[0][0]

# =========================
# RESULT
# =========================

print()
print("==============================")
print("RESULT")
print("==============================")

print("Raw prediction:", prediction)

if prediction >= 0.5:
    label = "DOG 🐶"
    confidence = prediction
else:
    label = "CAT 🐱"
    confidence = 1 - prediction

print("Prediction:", label)
print(f"Confidence: {confidence * 100:.2f}%")
print("==============================")