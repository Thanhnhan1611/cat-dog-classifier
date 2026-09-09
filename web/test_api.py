import requests

url = "http://127.0.0.1:5000/predict"

image_path = r"D:\py\cat-dog-classifier\test_image.jpg"

with open(image_path, "rb") as image:

    response = requests.post(
        url,
        files={
            "image": image
        }
    )

print("Status:", response.status_code)
print("Result:")
print(response.json())