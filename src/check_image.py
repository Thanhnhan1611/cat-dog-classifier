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

bad_images = []

print("Đang kiểm tra ảnh...\n")

for folder in folders:

    print(f"Checking: {folder}")

    for file in folder.iterdir():

        if not file.is_file():
            continue

        try:
            with Image.open(file) as img:
                # Kiểm tra file ảnh
                img.verify()

            # Mở lại để kiểm tra mode
            with Image.open(file) as img:
                img.load()

                if img.mode not in ["RGB", "RGBA", "L"]:
                    bad_images.append(
                        (file, f"Mode không hợp lệ: {img.mode}")
                    )

        except Exception as e:
            bad_images.append((file, str(e)))


print("\n==============================")
print("KẾT QUẢ")
print("==============================")

if len(bad_images) == 0:
    print("Không tìm thấy ảnh lỗi!")

else:
    print(f"Tìm thấy {len(bad_images)} ảnh có vấn đề:\n")

    for file, error in bad_images:
        print(f"{file}")
        print(f"  -> {error}")