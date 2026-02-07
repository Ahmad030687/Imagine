from flask import Flask, request, jsonify, send_file
import requests
import io
import os
import random

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 AHMAD RDX - Imagine Turbo API Active!"

@app.route('/api/imagine', methods=['GET'])
def ai_imagine():
    try:
        prompt = request.args.get('prompt')
        if not prompt:
            return jsonify({"status": False, "error": "Prompt missing"}), 400

        seed = random.randint(1, 9999999)
        
        # 🚀 Turbo Logic: Model ko 'flux-realism' ya 'flux' par rakha hai fast response ke liye
        # Is URL mein 'width' aur 'height' thori kam ki hai taake AI foran image de sake
        image_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?seed={seed}&width=720&height=720&model=flux&nologo=true"
        
        # ⏱️ Timeout 25 seconds rakha hai (Render ke 30 sec se pehle)
        try:
            img_resp = requests.get(image_url, timeout=25)
            img_resp.raise_for_status()
        except requests.exceptions.RequestException:
            # Agar primary server busy ho toh Backup server (Same provider, different route)
            backup_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?seed={seed}&width=512&height=512&nologo=true"
            img_resp = requests.get(backup_url, timeout=20)

        img_io = io.BytesIO(img_resp.content)
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/jpeg')

    except Exception as e:
        # User ko professional message bhejain
        return jsonify({
            "status": False, 
            "error": "AI Server is currently overloaded. Please try a simpler prompt or wait 10 seconds."
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
