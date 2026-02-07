from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os
import re

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 AHMAD RDX - Fake Number API (Fixed) Active!"

# ==========================================
# 📟 FIXED ENGINE: FAKE NUMBER SCRAPER
# ==========================================

@app.route('/api/sms/numbers', methods=['GET'])
def get_numbers():
    try:
        url = "https://receive-smss.com/"
        # Browser-like headers taake website ko lage asli banda hai
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://google.com"
        }
        
        resp = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        numbers_data = []
        
        # Method 1: Target specific card classes (Fixed selectors)
        boxes = soup.find_all('div', class_=re.compile(r'number-boxes-item'))
        
        if not boxes:
            # Method 2: Fallback - Page mein jitne bhi links hain jin mein numbers hain
            links = soup.find_all('a', href=re.compile(r'/sms/'))
            for link in links[:12]:
                num_text = link.text.strip()
                # Sirf numbers aur + sign nikaalna
                clean_num = re.sub(r'\D', '', num_text)
                if len(clean_num) > 5:
                    numbers_data.append({
                        "number": clean_num,
                        "country": "Global" 
                    })
        else:
            for box in boxes[:12]:
                try:
                    num = box.find('h4').get_text(strip=True).replace("+", "")
                    country = box.find('span', class_='number-boxes-item-m-country').get_text(strip=True)
                except:
                    # Agar country na mile toh link se number nikal lo
                    num = box.find('a')['href'].split('/')[-1]
                    country = "Unknown"
                
                numbers_data.append({"number": num, "country": country})
            
        return jsonify({
            "status": True, 
            "total": len(numbers_data),
            "numbers": numbers_data
        })
        
    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

@app.route('/api/sms/inbox', methods=['GET'])
def get_inbox():
    number = request.args.get('number')
    if not number:
        return jsonify({"status": False, "error": "Number missing"}), 400
    
    try:
        url = f"https://receive-smss.com/sms/{number}/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        resp = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        messages = []
        # Table rows nikaalna
        rows = soup.find_all('tr')
        
        for row in rows[1:7]: # Skip header row, take next 6
            tds = row.find_all('td')
            if len(tds) >= 3:
                messages.append({
                    "from": tds[0].get_text(strip=True),
                    "text": tds[2].get_text(strip=True),
                    "time": tds[3].get_text(strip=True) if len(tds) > 3 else "Recently"
                })
        
        return jsonify({"status": True, "number": number, "messages": messages})
        
    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
