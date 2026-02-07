from flask import Flask, request, jsonify, send_file
import requests
import io
import os
import asyncio
import edge_tts

app = Flask(__name__)

# 🔑 AAPKI PROVIDED COOKIE
COOKIE = "AEC=AVh_V2iyBHpOrwnn7CeXoAiedfWn9aarNoKT20Br2UX9Td9K-RAeS_o7Sg; HSID=Ao0szVfkYnMchTVfk; SSID=AGahZP8H4ni4UpnFV; APISID=SD-Q2DJLGdmZcxlA/AS8N0Gkp_b9sJC84f; SAPISID=9BY2tOwgEz4dK4dY/Acpw5_--fM7PV-aw4; __Secure-1PAPISID=9BY2tOwgEz4dK4dY/Acpw5_--fM7PV-aw4; __Secure-3PAPISID=9BY2tOwgEz4dK4dY/Acpw5_--fM7PV-aw4; SEARCH_SAMESITE=CgQI354B; SID=g.a0002wiVPDeqp9Z41WGZdsMDSNVWFaxa7cmenLYb7jwJzpe0kW3bZzx09pPfc201wUcRVKfh-wACgYKAXUSARMSFQHGX2MiU_dnPuMOs-717cJlLCeWOBoVAUF8yKpYTllPAbVgYQ0Mr_GyeXxV0076; __Secure-1PSID=g.a0002wiVPDeqp9Z41WGZdsMDSNVWFaxa7cmenLYb7jwJzpe0kW3b_Pt9L1eqcIAVeh7ZdRBOXgACgYKAYESARMSFQHGX2MicAK_Acu_-NCkzEz2wjCHmxoVAUF8yKp9xk8gQ82f-Ob76ysTXojB0076; __Secure-3PSID=g.a0002wiVPDeqp9Z41WGZdsMDSNVWFaxa7cmenLYb7jwJzpe0kW3bUudZTunPKtKbLRSoGKl1dAACgYKAYISARMSFQHGX2MimdzCEq63UmiyGU-3eyZx9RoVAUF8yKrc4ycLY7LGaJUyDXk_7u7M0076"

@app.route('/')
def home():
    return "🦅 AHMAD RDX - Ultimate API Engine Fixed!"

# ==========================================
# 🔊 ENGINE 1: VOICE (Edge TTS - Unstoppable)
# ==========================================
@app.route('/api/voice', methods=['GET'])
def speak():
    try:
        text = request.args.get('text')
        if not text: return "Text missing", 400
        
        async def generate():
            communicate = edge_tts.Communicate(text, "ur-PK-AsadNeural")
            data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio": data += chunk["data"]
            return data

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio = loop.run_until_complete(generate())
        return send_file(io.BytesIO(audio), mimetype='audio/mpeg')
    except Exception as e: return str(e), 500

# ==========================================
# 🎨 ENGINE 2: IMAGINE & LOGO (NanoBanana Gemini)
# ==========================================
@app.route('/api/generate', methods=['GET'])
def generate_img():
    try:
        prompt = request.args.get('prompt')
        style = request.args.get('style', 'none') # modern, esports, luxury or none

        if not prompt: return "Prompt missing", 400

        # Agar style 'none' nahi hai, toh prompt ko logo ke liye lapet lo
        if style != 'none':
            if style == 'luxury': prompt = f"Create a luxury premium gold logo for '{prompt}', black background, high-end."
            elif style == 'esports': prompt = f"Fierce esports mascot logo for '{prompt}', neon colors, bold typography."
            else: prompt = f"Professional minimalist vector logo for '{prompt}', clean lines."

        # NanoBanana Fixed Logic
        api_url = "https://anabot.my.id/api/ai/geminiOption"
        params = {
            "prompt": prompt,
            "type": "NanoBanana",
            "imageUrl": "", # Khali string dena zaroori hai
            "cookie": COOKIE,
            "apikey": "freeApikey"
        }

        resp = requests.get(api_url, params=params, timeout=60)
        res_data = resp.json()

        if res_data.get('success'):
            img_url = res_data['data']['result']['url']
            img_bytes = requests.get(img_url).content
            return send_file(io.BytesIO(img_bytes), mimetype='image/png')
        else:
            return jsonify({"status": False, "error": res_data.get('error')}), 500

    except Exception as e: return str(e), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    
