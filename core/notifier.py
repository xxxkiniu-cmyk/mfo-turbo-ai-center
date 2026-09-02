import requests

TOKEN = "8973202046:AAFABI_L83kYX6GtLjtJwc6q4wHtBRR8db4"
CHAT_ID = "8695401493"

def send(title, message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": f"*{title}*\n\n{message}",
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=payload)
        return response.json()
    except Exception as e:
        return {"ok": False, "description": str(e)}

if __name__ == "__main__":
    res = send("🚀 MFO.ai - Test Notifiera", "System powiadomień działa poprawnie!")
    print(res)
