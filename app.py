import random

@app.route('/api/imagine', methods=['GET'])
def ai_imagine():
    try:
        prompt = request.args.get('prompt')
        if not prompt:
            return jsonify({"status": False, "error": "Prompt missing"}), 400

        # High Quality AI Image Generator (Flux/Stable Diffusion XL)
        seed = random.randint(1, 999999)
        # 2026 High-speed AI endpoint
        image_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?seed={seed}&width=1024&height=1024&model=flux&nologo=true"
        
        # Image download kar ke direct bhejain taake bot ko buffering na karni paray
        img_resp = requests.get(image_url, timeout=30)
        
        img_io = io.BytesIO(img_resp.content)
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500
