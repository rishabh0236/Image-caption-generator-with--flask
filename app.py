from flask import Flask, request, jsonify, render_template
from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
import torch
from PIL import Image

app = Flask(__name__)

model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

max_length = 16
num_captions = 5


@app.route("/generate-caption", methods=["POST"])
def generate_caption():
    images = []
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"})

    image_file = request.files["image"]
    image_path = "./static/{}".format(image_file.filename)
    image_file.save(image_path)
    
    image = Image.open(image_file)
    if image.mode != "RGB":
        image = image.convert(mode="RGB")
    images.append(image)
    #images = [image]

    pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    preds = []
    for _ in range(num_captions):
        output_ids = model.generate(pixel_values, max_length=max_length, do_sample=True, num_return_sequences=1)
        caption = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
        preds.append(caption)

    captions = [f"{i+1}. {caption}" for i, caption in enumerate(preds)]

    return jsonify({"image": image_path, "captions": captions})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
    
