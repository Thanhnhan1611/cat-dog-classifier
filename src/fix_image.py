from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

folders = [
    DATA_DIR / "train" / "cat",
    DATA_DIR / "train" / "dog",
    DATA_DIR / "val" / "cat",
    DATA_DIR / "val" / "dog",
    DATA_DIR / "test" / "cat",
    DATA_DIR / "test" / "dog",
]

converted = 0
bad_images = []

print("Bắt đầu xử lý ảnh...\n")

for folder in folders:

    print(f"Checking: {folder}")

    for file in folder.iterdir():

        if not file.is_file():
            continue

        try:
            with Image.open(file) as img:

                # Đảm bảo ảnh được đọc hoàn chỉnh
                img.load()

                # Chuyển tất cả ảnh không phải RGB/RGBA về RGB
                if img.mode not in ["RGB", "RGBA"]:
                    print(f"Convert: {file.name} ({img.mode} -> RGB)")

                    converted_img = img.convert("RGB")

                    # Ghi đè file cũ
                    converted_img.save(
                        file,
                        format="JPEG",
                        quality=95
                    )

                    converted += 1

        except Exception as e:
            print(f"ẢNH LỖI: {file}")
            print(f"  -> {e}")

            bad_images.append(file)


print("\n==============================")
print("KẾT QUẢ")
print("==============================")

print(f"Ảnh đã chuyển sang RGB: {converted}")
print(f"Ảnh lỗi không xử lý được: {len(bad_images)}")

if bad_images:
    print("\nDanh sách ảnh lỗi:")

    for file in bad_images:
        print(file)

else:
    print("\nKhông còn ảnh lỗi!")