from flask import Flask, request, jsonify, send_file
import requests
import io
import os

app = Flask(__name__)

# 🔑 Aap ki ElevenLabs Key
ELEVEN_API_KEY = "sk_377990659c6de5643f922fa60e3e3c0850e09c8d06ce1cfd"

@app.route('/')
def home():
    return "🦅 AHMAD RDX - Voice Cloning Engine Active!"

# ==========================================
# 🎭 STEP 1: VOICE CLONE (Upload & Get ID)
# ==========================================
@app.route('/api/voice/clone', methods=['POST'])
def clone_voice():
    try:
        data = request.json
        audio_url = data.get('audio_url')
        voice_name = data.get('name', 'Cloned_AhmadRDX')

        if not audio_url:
            return jsonify({"status": False, "error": "Audio URL missing"}), 400

        # Audio download karna
        audio_resp = requests.get(audio_url)
        audio_file = io.BytesIO(audio_resp.content)

        # ElevenLabs "Add Voice" API
        url = "https://api.elevenlabs.io/v1/voices/add"
        headers = {"xi-api-key": ELEVEN_API_KEY}
        files = {
            'files': ('sample.mp3', audio_file, 'audio/mpeg'),
            'name': (None, voice_name),
            'description': (None, "Cloned via Ahmad RDX Bot")
        }

        resp = requests.post(url, headers=headers, files=files)
        res_data = resp.json()

        if resp.status_code == 200:
            return jsonify({"status": True, "voice_id": res_data['voice_id']})
        else:
            return jsonify({"status": False, "error": res_data}), resp.status_code

    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

# ==========================================
# 🎙️ STEP 2: VOICE SPEAK (Using Voice ID)
# ==========================================
@app.route('/api/voice/speak', methods=['GET'])
def speak_voice():
    try:
        text = request.args.get('text')
        voice_id = request.args.get('voice_id')

        if not text or not voice_id:
            return jsonify({"status": False, "error": "Params missing"}), 400

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVEN_API_KEY
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2", # Best for Urdu/Hindi
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        }

        resp = requests.post(url, json=data, headers=headers)

        if resp.status_code == 200:
            audio_io = io.BytesIO(resp.content)
            audio_io.seek(0)
            return send_file(audio_io, mimetype='audio/mpeg')
        else:
            return jsonify({"status": False, "error": "API Error"}), resp.status_code

    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
