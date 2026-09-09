import tensorflow as tf
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
folders = [
    ROOT / "data" / "train" / "cat",
    ROOT / "data" / "train" / "dog",
    ROOT / "data" / "val" / "cat",
    ROOT / "data" / "val" / "dog",
    ROOT / "data" / "test" / "cat",
    ROOT / "data" / "test" / "dog",
]

bad_files = []

for folder in folders:
    print(f"\nĐang kiểm tra: {folder}")

    for file in folder.iterdir():
        if file.suffix.lower() not in [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"]:
            continue

        try:
            data = tf.io.read_file(str(file))
            image = tf.io.decode_image(
                data,
                channels=3,
                expand_animations=False
            )

            # Kiểm tra TensorFlow có đọc được kích thước không
            _ = image.shape

        except Exception as e:
            print("❌ LỖI:", file)
            print("   ", str(e)[:300])
            bad_files.append(file)

print("\n" + "=" * 50)
print(f"TỔNG SỐ ẢNH LỖI: {len(bad_files)}")
print("=" * 50)

for file in bad_files:
    print(file)