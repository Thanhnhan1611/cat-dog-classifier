import tensorflow as tf
from tensorflow.keras import layers

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# Load dataset
train_data = tf.keras.utils.image_dataset_from_directory(
    "../data/train",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True
)

val_data = tf.keras.utils.image_dataset_from_directory(
    "../data/val",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

test_data = tf.keras.utils.image_dataset_from_directory(
    "../data/test",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

# Data augmentation
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])

# Chuẩn hóa pixel
normalization = layers.Rescaling(1./255)

# Test preprocessing
images, labels = next(iter(train_data))

augmented_images = data_augmentation(images)
normalized_images = normalization(augmented_images)

print("Ảnh gốc:", images.shape)
print("Ảnh sau augmentation:", augmented_images.shape)
print("Pixel nhỏ nhất:", tf.reduce_min(normalized_images).numpy())
print("Pixel lớn nhất:", tf.reduce_max(normalized_images).numpy())
