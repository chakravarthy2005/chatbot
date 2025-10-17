from flask import Flask, request, jsonify
import google.generativeai as genai
import vonage

# ---------------- HARD-CODED CONFIG ----------------
GENIE_API_KEY = "AIzaSyB0hthTJPT8XadaB7GkA3w0Gy5QKPyLVm4"
VONAGE_API_KEY = "9e21dc3a"
VONAGE_API_SECRET = "cttBO%SJicxArD$sd5GlBI*5"
WHATSAPP_NUMBER = "14157386102"
USER_NUMBER = "918660029082"

# ---------------- INITIALIZE ----------------
genai.configure(api_key=GENIE_API_KEY)
model = genai.GenerativeModel("models/gemini-2.0-flash")

# ---------------- VONAGE ----------------
messaging = vonage.Messaging(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)

# ---------------- FLASK ----------------
app = Flask(__name__)

def gk_answer(question: str):
    prompt = f"You are a general knowledge assistant. Answer in one short paragraph.\n\nQuestion: {question}"
    response = model.generate_content(prompt)
    return response.text.strip()

def send_whatsapp(text):
    message = {
        "channel": "whatsapp",
        "message_type": "text",
        "to": USER_NUMBER,
        "from": WHATSAPP_NUMBER,
        "text": text
    }
    resp = messaging.send_message(message)
    print("Vonage Response:", resp)
    return resp

@app.route("/", methods=["GET"])
def home():
    return "✅ GK WhatsApp Chatbot is running."

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    user_msg = data.get("message", {}).get("content", {}).get("text")
    if not user_msg:
        user_msg = str(data)
    answer = gk_answer(user_msg)
    send_whatsapp(answer)
    return jsonify({"status": "ok", "question": user_msg, "answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
