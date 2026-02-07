from flask import Flask, request, jsonify, send_file
import requests
import io
import os

app = Flask(__name__)

# 🔑 Aap ki ElevenLabs Key
ELEVEN_API_KEY = "sk_377990659c6de5643f922fa60e3e3c0850e09c8d06ce1cfd"

@app.route('/')
def home():
    return "🦅 AHMAD RDX - Voice Engine Active!"

# ==========================================
# 🎭 CLONE ENDPOINT
# ==========================================
@app.route('/api/voice/clone', methods=['POST'])
def clone_voice():
    try:
        data = request.json
        audio_url = data.get('audio_url')
        if not audio_url:
            return jsonify({"status": False, "error": "Audio URL missing"}), 400

        audio_resp = requests.get(audio_url)
        audio_file = io.BytesIO(audio_resp.content)

        url = "https://api.elevenlabs.io/v1/voices/add"
        headers = {"xi-api-key": ELEVEN_API_KEY}
        files = {
            'files': ('sample.mp3', audio_file, 'audio/mpeg'),
            'name': (None, "Cloned_Voice"),
        }

        resp = requests.post(url, headers=headers, files=files)
        
        # 🛡️ DEBUGGING: Agar error aaye toh ElevenLabs ka asli message dikhao
        if resp.status_code != 200:
            return jsonify({"status": False, "error": "ElevenLabs Rejected", "details": resp.json()}), resp.status_code

        return jsonify({"status": True, "voice_id": resp.json()['voice_id']})

    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

# ==========================================
# 🎙️ SPEAK ENDPOINT
# ==========================================
@app.route('/api/voice/speak', methods=['GET'])
def speak_voice():
    try:
        text = request.args.get('text')
        voice_id = request.args.get('voice_id')
        if not text or not voice_id:
            return jsonify({"status": False, "error": "Params missing"}), 400

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {"xi-api-key": ELEVEN_API_KEY, "Content-Type": "application/json"}
        data = {"text": text, "model_id": "eleven_multilingual_v2"}

        resp = requests.post(url, json=data, headers=headers)

        if resp.status_code == 200:
            return send_file(io.BytesIO(resp.content), mimetype='audio/mpeg')
        else:
            return jsonify({"status": False, "error": "Speak Fail", "details": resp.json()}), resp.status_code

    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    
