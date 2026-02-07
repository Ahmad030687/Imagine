from flask import Flask, request, jsonify, send_file
import requests
import io
import os

app = Flask(__name__)

# 🔑 AAPKI PROVIDED COOKIE (Securely placed in Backend)
COOKIE = "AEC=AVh_V2iyBHpOrwnn7CeXoAiedfWn9aarNoKT20Br2UX9Td9K-RAeS_o7Sg; HSID=Ao0szVfkYnMchTVfk; SSID=AGahZP8H4ni4UpnFV; APISID=SD-Q2DJLGdmZcxlA/AS8N0Gkp_b9sJC84f; SAPISID=9BY2tOwgEz4dK4dY/Acpw5_--fM7PV-aw4; __Secure-1PAPISID=9BY2tOwgEz4dK4dY/Acpw5_--fM7PV-aw4; __Secure-3PAPISID=9BY2tOwgEz4dK4dY/Acpw5_--fM7PV-aw4; SEARCH_SAMESITE=CgQI354B; SID=g.a0002wiVPDeqp9Z41WGZdsMDSNVWFaxa7cmenLYb7jwJzpe0kW3bZzx09pPfc201wUcRVKfh-wACgYKAXUSARMSFQHGX2MiU_dnPuMOs-717cJlLCeWOBoVAUF8yKpYTllPAbVgYQ0Mr_GyeXxV0076; __Secure-1PSID=g.a0002wiVPDeqp9Z41WGZdsMDSNVWFaxa7cmenLYb7jwJzpe0kW3b_Pt9L1eqcIAVeh7ZdRBOXgACgYKAYESARMSFQHGX2MicAK_Acu_-NCkzEz2wjCHmxoVAUF8yKp9xk8gQ82f-Ob76ysTXojB0076; __Secure-3PSID=g.a0002wiVPDeqp9Z41WGZdsMDSNVWFaxa7cmenLYb7jwJzpe0kW3bUudZTunPKtKbLRSoGKl1dAACgYKAYISARMSFQHGX2MimdzCEq63UmiyGU-3eyZx9RoVAUF8yKrc4ycLY7LGaJUyDXk_7u7M0076"

@app.route('/')
def home():
    return "🦅 AHMAD RDX - NanoBanana Pro Logo API Active!"

# ==========================================
# 🎨 ENGINE: LOGO PRO (GEMINI NANOBANANA)
# ==========================================
@app.route('/api/logo_pro', methods=['GET'])
def generate_logo():
    try:
        text = request.args.get('text')
        style = request.args.get('style', 'modern').lower()

        if not text:
            return jsonify({"status": False, "error": "Brand name missing"}), 400

        # 🤫 HEAVY PROMPT ENGINEERING
        # Hum Gemini ko bata rahe hain ke bacho wali pic nahi, professional logo chahiye.
        prompts = {
            'modern': f"Create a professional minimalist vector logo for the brand '{text}'. Clean geometric lines, corporate aesthetic, high-end design, white background, 4k.",
            'esports': f"Create a fierce esports mascot logo for team '{text}'. Aggressive character design, neon glowing colors, bold gaming typography, shield background, ultra-detailed.",
            'luxury': f"Create a luxury premium logo for '{text}'. Metallic gold embossed texture, elegant serif font, black leather background, sophisticated brand identity."
        }

        final_prompt = prompts.get(style, prompts['modern'])
        
        # NanoBanana API Call
        # Note: Text-to-image ke liye imageUrl ko khali rakha hai ya prompt mein handle kiya hai
        api_url = f"https://anabot.my.id/api/ai/geminiOption"
        params = {
            "prompt": final_prompt,
            "type": "NanoBanana",
            "cookie": COOKIE,
            "apikey": "freeApikey"
        }

        resp = requests.get(api_url, params=params, timeout=60)
        data = resp.json()

        if data.get('success'):
            result_url = data['data']['result']['url']
            img_data = requests.get(result_url).content
            return send_file(io.BytesIO(img_data), mimetype='image/png')
        else:
            return jsonify({"status": False, "error": data.get('error', 'API Failed'), "details": data}), 500

    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
