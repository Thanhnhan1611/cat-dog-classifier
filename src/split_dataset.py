from pathlib import Path
import random
import shutil

# Lấy thư mục gốc của project
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

# Các thư mục
TRAIN_CAT = DATA_DIR / "train" / "cat"
TRAIN_DOG = DATA_DIR / "train" / "dog"

VAL_CAT = DATA_DIR / "val" / "cat"
VAL_DOG = DATA_DIR / "val" / "dog"

TEST_CAT = DATA_DIR / "test" / "cat"
TEST_DOG = DATA_DIR / "test" / "dog"

# Tạo thư mục nếu chưa tồn tại
for folder in [VAL_CAT, VAL_DOG, TEST_CAT, TEST_DOG]:
    folder.mkdir(parents=True, exist_ok=True)


def split_class(source_folder, val_folder, test_folder):
    # Lấy tất cả file ảnh
    files = [
        f for f in source_folder.iterdir()
        if f.is_file()
    ]

    print(f"\nThư mục: {source_folder}")
    print(f"Tổng số ảnh: {len(files)}")

    # Trộn ngẫu nhiên
    random.shuffle(files)

    # 10% validation
    val_count = int(len(files) * 0.10)

    # 10% test
    test_count = int(len(files) * 0.10)

    val_files = files[:val_count]
    test_files = files[val_count:val_count + test_count]

    # Di chuyển ảnh sang validation
    for file in val_files:
        shutil.move(str(file), str(val_folder / file.name))

    # Di chuyển ảnh sang test
    for file in test_files:
        shutil.move(str(file), str(test_folder / file.name))

    print(f"Đã chuyển sang validation: {len(val_files)}")
    print(f"Đã chuyển sang test: {len(test_files)}")
    print(f"Còn lại trong train: {len(files) - len(val_files) - len(test_files)}")


# Cố định kết quả random
random.seed(42)

# Chia cat
split_class(
    TRAIN_CAT,
    VAL_CAT,
    TEST_CAT
)

# Chia dog
split_class(
    TRAIN_DOG,
    VAL_DOG,
    TEST_DOG
)

print("\n==============================")
print("CHIA DATASET HOÀN TẤT!")
print("==============================")