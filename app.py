from flask import Flask, request, jsonify, send_file
import requests
import io
import os
import random

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 AHMAD RDX - Multi-Engine Imagine API Active!"

def fetch_image(url, timeout_val):
    resp = requests.get(url, timeout=timeout_val)
    if resp.status_code == 200 and 'image' in resp.headers.get('Content-Type', ''):
        return resp.content
    return None

@app.route('/api/imagine', methods=['GET'])
def ai_imagine():
    try:
        prompt = request.args.get('prompt')
        if not prompt:
            return jsonify({"status": False, "error": "Prompt missing"}), 400

        seed = random.randint(1, 9999999)
        prompt_encoded = prompt.replace(' ', '%20')

        # --- ENGINE 1: Pollinations (Flux) ---
        url1 = f"https://image.pollinations.ai/prompt/{prompt_encoded}?seed={seed}&width=720&height=720&model=flux&nologo=true"
        
        # --- ENGINE 2: Backup (Stable Diffusion / Turbo) ---
        url2 = f"https://image.pollinations.ai/prompt/{prompt_encoded}?seed={seed}&width=512&height=512&nologo=true"

        # Koshish 1
        print(f"Trying Engine 1 for: {prompt}")
        img_data = fetch_image(url1, 20)

        # Agar 1 fail ho jaye, toh Koshish 2
        if not img_data:
            print("Engine 1 failed or busy. Switching to Engine 2...")
            img_data = fetch_image(url2, 15)

        if img_data:
            img_io = io.BytesIO(img_data)
            img_io.seek(0)
            return send_file(img_io, mimetype='image/jpeg')
        else:
            return jsonify({
                "status": False, 
                "error": "All AI Engines are currently busy. Please try again in 30 seconds."
            }), 503

    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
