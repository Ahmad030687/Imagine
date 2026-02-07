from flask import Flask, request, jsonify, send_file
import requests
import io
import os
import random

# App define karna sabse zaroori hai
app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 AHMAD RDX - Final Imagine API Active!"

# ==========================================
# 🎨 ONLY AI IMAGINE (FLUX MODEL - STABLE)
# ==========================================
@app.route('/api/imagine', methods=['GET'])
def ai_imagine():
    try:
        prompt = request.args.get('prompt')
        if not prompt:
            return jsonify({"status": False, "error": "Prompt missing"}), 400

        # Seed random rakha hai taake har baar alag result aaye
        seed = random.randint(1, 9999999)
        
        # 🚀 Flux Model - 720x720 (Best balance for Render speed)
        image_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?seed={seed}&width=720&height=720&model=flux&nologo=true"
        
        print(f"Generating: {prompt}") # Render logs ke liye

        # ⏱️ Timeout 28 seconds (Render ka limit 30s hai)
        img_resp = requests.get(image_url, timeout=28)
        
        # 🛡️ CRITICAL CHECKS (Broken Icon Fix)
        # 1. Agar AI server busy hai ya error diya (e.g. 500, 503, 404)
        if img_resp.status_code != 200:
            return jsonify({
                "status": False, 
                "error": f"AI Server Busy (Status: {img_resp.status_code}). Please try again."
            }), 502

        # 2. Agar response image nahi hai ya khali hai (Corrupted data)
        content_type = img_resp.headers.get('Content-Type', '')
        if 'image' not in content_type or len(img_resp.content) < 1000:
             return jsonify({
                "status": False, 
                "error": "AI generated corrupted data. Try a different prompt."
            }), 500

        # Agar sab theek hai, tabhi image bhejain
        img_io = io.BytesIO(img_resp.content)
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/jpeg')

    except requests.exceptions.Timeout:
        # Agar 28 second tak image nahi bani
        return jsonify({"status": False, "error": "Generation timed out. AI is very busy, try again in 1 minute."}), 504
    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

if __name__ == "__main__":
    # Render ke liye port setup
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
