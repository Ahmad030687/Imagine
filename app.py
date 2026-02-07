from flask import Flask, request, jsonify, send_file
import requests
import io
import os

app = Flask(__name__)

# 🔑 AAPKI PROVIDED COOKIE
COOKIE = "AEC=AVh_V2iyBHpOrwnn7CeXoAiedfWn9aarNoKT20Br2UX9Td9K-RAeS_o7Sg; ..." # (Yahan apni pori cookie lagayein)

@app.route('/')
def home():
    return "🦅 AHMAD RDX - Multi-Purpose Gemini AI Engine Active!"

# ==========================================
# 🎨 ENGINE: IMAGINATION PRO (General Text-to-Image)
# ==========================================
@app.route('/api/imagine_pro', methods=['GET'])
def imagine_pro():
    try:
        prompt = request.args.get('prompt')
        if not prompt:
            return jsonify({"status": False, "error": "Prompt is missing"}), 400

        # NanoBanana API Call
        api_url = f"https://anabot.my.id/api/ai/geminiOption"
        params = {
            "prompt": f"Ultra realistic, 8k resolution, highly detailed: {prompt}",
            "type": "NanoBanana",
            "cookie": COOKIE,
            "apikey": "freeApikey"
        }

        resp = requests.get(api_url, params=params, timeout=80)
        data = resp.json()

        if data.get('success'):
            result_url = data['data']['result']['url']
            img_data = requests.get(result_url).content
            return send_file(io.BytesIO(img_data), mimetype='image/png')
        else:
            return jsonify({"status": False, "error": "AI failed to generate image"}), 500

    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

# (Puraani logo_pro logic bhi iske niche rehne dein)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    
