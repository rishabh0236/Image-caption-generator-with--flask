<script>
    const form = document.querySelector("form");
    const uploadedImage = document.getElementById("uploaded-image");
    const captionsDiv = document.getElementById("captions");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const response = await fetch("/generate-caption", {
            method: "POST",
            body: formData
        });
        const data = await response.json();

        // Set the uploaded image source
        uploadedImage.src = data.image;

        // Clear previous captions
        captionsDiv.innerHTML = "";

        // Display captions with numbers and line breaks
        data.captions.forEach((caption, index) => {
            const p = document.createElement("p");
            p.innerHTML = `${index + 1}. ${caption}`;
            captionsDiv.appendChild(p);
        });
    });
</script>
