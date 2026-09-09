const imageInput = document.getElementById("imageInput");
const selectButton = document.getElementById("selectButton");

const previewContainer = document.getElementById("previewContainer");
const previewImage = document.getElementById("previewImage");

const predictButton = document.getElementById("predictButton");

const loading = document.getElementById("loading");
const result = document.getElementById("result");

const resultIcon = document.getElementById("resultIcon");
const resultLabel = document.getElementById("resultLabel");

const confidenceFill = document.getElementById("confidenceFill");
const confidenceText = document.getElementById("confidenceText");


// ==============================
// CHỌN ẢNH
// ==============================

selectButton.addEventListener("click", function () {

    imageInput.click();

});


// ==============================
// HIỂN THỊ PREVIEW
// ==============================

imageInput.addEventListener("change", function () {

    const file = imageInput.files[0];

    if (!file) {
        return;
    }

    // Kiểm tra file có phải ảnh không
    if (!file.type.startsWith("image/")) {

        alert("Vui lòng chọn một file ảnh!");

        imageInput.value = "";

        return;
    }

    // Tạo preview
    const imageURL = URL.createObjectURL(file);

    previewImage.src = imageURL;

    previewContainer.style.display = "flex";

    result.style.display = "none";

});


// ==============================
// NHẬN DIỆN
// ==============================

predictButton.addEventListener("click", async function () {

    const file = imageInput.files[0];

    if (!file) {

        alert("Vui lòng chọn ảnh trước!");

        return;
    }


    // Hiển thị loading
    previewContainer.style.display = "none";

    loading.style.display = "block";

    result.style.display = "none";


    // Tạo FormData
    const formData = new FormData();

    formData.append("image", file);


    try {

        // Gửi ảnh tới Flask
        const response = await fetch(
            "/predict",
            {
                method: "POST",
                body: formData
            }
        );


        const data = await response.json();


        // Kiểm tra lỗi
        if (!response.ok) {

            throw new Error(
                data.error || "Có lỗi xảy ra!"
            );

        }


        // ==============================
        // HIỂN THỊ KẾT QUẢ
        // ==============================

        resultLabel.textContent =
            data.prediction;

        confidenceText.textContent =
            data.confidence + "%";


        confidenceFill.style.width =
            data.confidence + "%";


        // Icon
        if (data.prediction === "CAT") {

            resultIcon.textContent = "🐱";

        } else {

            resultIcon.textContent = "🐶";

        }


        // Hiển thị
        loading.style.display = "none";

        result.style.display = "block";


    } catch (error) {

        loading.style.display = "none";

        previewContainer.style.display = "flex";

        alert(
            "Không thể nhận diện ảnh:\n" +
            error.message
        );

    }

});