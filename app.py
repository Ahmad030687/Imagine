from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

# 1. Sabse pehle app define karna zaroori hai (NameError se bachne ke liye)
app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 AHMAD RDX - Fake Number SMS API Active!"

# ==========================================
# 📟 ENGINE: FAKE NUMBER & SMS RECEIVER
# ==========================================

# Endpoint 1: Numbers ki list nikaalne ke liye
@app.route('/api/sms/numbers', methods=['GET'])
def get_numbers():
    try:
        url = "https://receive-smss.com/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        resp = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        numbers_data = []
        # Website ke boxes se data nikaalna
        boxes = soup.select(".number-boxes-item-m")
        
        for box in boxes[:12]: # Pehle 12 numbers nikaal rahe hain
            number = box.select_one("h4").text.strip().replace("+", "")
            country = box.select_one(".number-boxes-item-m-country").text.strip()
            numbers_data.append({
                "number": number,
                "country": country
            })
            
        return jsonify({
            "status": True, 
            "total": len(numbers_data),
            "numbers": numbers_data
        })
        
    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

# Endpoint 2: Specific Number ka Inbox check karne ke liye
@app.route('/api/sms/inbox', methods=['GET'])
def get_inbox():
    number = request.args.get('number') # e.g. 447496032123
    if not number:
        return jsonify({"status": False, "error": "Number parameter is missing"}), 400
    
    try:
        # Number ke specific page par jana
        url = f"https://receive-smss.com/sms/{number}/"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        resp = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        messages = []
        # Inbox table se latest SMS rows nikaalna
        table_rows = soup.select("#msgtbl tbody tr")
        
        for row in table_rows[:6]: # Latest 6 messages
            tds = row.select("td")
            if len(tds) >= 4:
                sender = tds[0].text.strip()
                content = tds[2].text.strip()
                time_ago = tds[3].text.strip()
                
                messages.append({
                    "from": sender,
                    "text": content,
                    "time": time_ago
                })
        
        return jsonify({
            "status": True,
            "number": number,
            "messages": messages
        })
        
    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

# ==========================================
# 🚀 RENDER DEPLOYMENT SETTINGS
# ==========================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
