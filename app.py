from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import os, uuid

app = Flask(__name__)

OUTPUT_DIR = "generated"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/")
def home():
    return "AHMAD RDX TEXT TO IMAGE API RUNNING"

@app.route("/api/text2img", methods=["GET"])
def text_to_image():
    text = request.args.get("text")
    color = request.args.get("color", "white")

    if not text:
        return jsonify({"status": False, "error": "text missing"})

    # image
    img = Image.new("RGB", (800, 400), color="black")
    draw = ImageDraw.Draw(img)

    # default font
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()

    # center text
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    x = (800 - w) // 2
    y = (400 - h) // 2

    draw.text((x, y), text, fill=color, font=font)

    # save
    filename = f"{uuid.uuid4()}.png"
    path = os.path.join(OUTPUT_DIR, filename)
    img.save(path)

    return jsonify({
        "status": True,
        "image": request.host_url + "result/" + filename,
        "creator": "AHMAD RDX"
    })

@app.route("/result/<name>")
def result(name):
    return send_file(os.path.join(OUTPUT_DIR, name), mimetype="image/png")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
