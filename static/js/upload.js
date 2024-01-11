document.addEventListener("DOMContentLoaded", function () {
    const dragDropArea = document.getElementById("drag-drop-area");
    const imageUpload = document.getElementById("image-upload");
    const uploadedImage = document.getElementById("uploaded-image");

    function displayImage(file) {
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                uploadedImage.src = e.target.result;
                uploadedImage.style.display = "block";
            };
            reader.readAsDataURL(file);
        }
    }

    function resizeImage(file, callback) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement("canvas");
                const ctx = canvas.getContext("2d");

                canvas.width = 224;
                canvas.height = 224;

                ctx.drawImage(img, 0, 0, 224, 224);

                canvas.toBlob((blob) => {
                    callback(blob);
                }, "image/jpeg", 0.8);
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }

    dragDropArea.addEventListener("dragover", (e) => {
        e.preventDefault();
        dragDropArea.style.backgroundColor = "#ddd";
    });

    dragDropArea.addEventListener("dragleave", () => {
        dragDropArea.style.backgroundColor = "#f1f1f1";
    });

    dragDropArea.addEventListener("drop", (e) => {
        e.preventDefault();
        dragDropArea.style.backgroundColor = "#f1f1f1";
        const file = e.dataTransfer.files[0];
        resizeImage(file, (resizedBlob) => {
            displayImage(resizedBlob);
        });
    });

    dragDropArea.addEventListener("click", () => {
        imageUpload.click();
    });

    imageUpload.addEventListener("change", () => {
        const file = imageUpload.files[0];
        resizeImage(file, (resizedBlob) => {
            displayImage(resizedBlob);
        });
    });

    document.getElementById("image-upload").addEventListener("change", function () {
        var input = this;

        if (input.files && input.files[0]) {
            resizeImage(input.files[0], (resizedBlob) => {
                displayImage(resizedBlob);
            });
        }
    });
});
