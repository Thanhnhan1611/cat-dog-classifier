import tensorflow as tf

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

train_dir = "../data/train"
val_dir = "../data/val"
test_dir = "../data/test"

train_data = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True
)

val_data = tf.keras.utils.image_dataset_from_directory(
    val_dir,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

test_data = tf.keras.utils.image_dataset_from_directory(
    test_dir,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

print("Classes:", train_data.class_names)

print("Train batches:", len(train_data))
print("Validation batches:", len(val_data))
print("Test batches:", len(test_data))