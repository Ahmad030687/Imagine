from flask import Flask, request, jsonify, send_file
import requests
import io
import os
import random

# App define karna sabse zaroori hai
app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 AHMAD RDX - Akeli Imagine AI API Active!"

# ==========================================
# 🎨 ONLY AI IMAGINE (FLUX MODEL)
# ==========================================
@app.route('/api/imagine', methods=['GET'])
def ai_imagine():
    try:
        prompt = request.args.get('prompt')
        if not prompt:
            return jsonify({"status": False, "error": "Prompt missing"}), 400

        # Seed random rakha hai taake har baar alag result aaye
        seed = random.randint(1, 9999999)
        
        # 2026 Flux Model (Best for Text and Details)
        image_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?seed={seed}&width=1024&height=1024&model=flux&nologo=true"
        
        # Image fetch karna
        img_resp = requests.get(image_url, timeout=40)
        
        if img_resp.status_code != 200:
            return jsonify({"status": False, "error": "AI Server didn't respond"}), 500

        img_io = io.BytesIO(img_resp.content)
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/jpeg')

    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

if __name__ == "__main__":
    # Render ke liye port setup
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
