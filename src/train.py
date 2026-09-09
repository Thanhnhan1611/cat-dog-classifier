import tensorflow as tf
from tensorflow.keras import layers, models
from pathlib import Path

# =========================
# CẤU HÌNH
# =========================

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 5

ROOT = Path(__file__).resolve().parent.parent

TRAIN_DIR = ROOT / "data" / "train"
VAL_DIR = ROOT / "data" / "val"
TEST_DIR = ROOT / "data" / "test"
MODEL_DIR = ROOT / "models"

# =========================
# LOAD DATASET
# =========================

train_data = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True
)

val_data = tf.keras.utils.image_dataset_from_directory(
    VAL_DIR,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

test_data = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

print("Classes:", train_data.class_names)

# =========================
# TỐI ƯU DATA PIPELINE
# =========================

AUTOTUNE = tf.data.AUTOTUNE

train_data = train_data.prefetch(AUTOTUNE)
val_data = val_data.prefetch(AUTOTUNE)
test_data = test_data.prefetch(AUTOTUNE)

# =========================
# DATA AUGMENTATION
# =========================

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])

# =========================
# MOBILENETV2
# =========================

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)

# Đóng băng MobileNetV2
base_model.trainable = False

# =========================
# BUILD MODEL
# =========================

inputs = layers.Input(shape=(224, 224, 3))

x = data_augmentation(inputs)

# MobileNetV2 cần input theo preprocessing của nó
x = tf.keras.applications.mobilenet_v2.preprocess_input(x)

x = base_model(x, training=False)

x = layers.GlobalAveragePooling2D()(x)

x = layers.Dropout(0.3)(x)

outputs = layers.Dense(1, activation="sigmoid")(x)

model = models.Model(inputs, outputs)

# =========================
# COMPILE
# =========================

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# =========================
# TRAIN
# =========================

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS
)

# =========================
# TEST
# =========================

test_loss, test_accuracy = model.evaluate(test_data)

print("\n==============================")
print("TEST RESULTS")
print("==============================")
print("Test loss:", test_loss)
print("Test accuracy:", test_accuracy)

# =========================
# SAVE MODEL
# =========================

MODEL_DIR.mkdir(exist_ok=True)

model_path = MODEL_DIR / "cat_dog_mobilenetv2.keras"

model.save(model_path)

print("\nModel đã được lưu tại:")
print(model_path)