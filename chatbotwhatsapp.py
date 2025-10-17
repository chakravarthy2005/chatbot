from flask import Flask, request, jsonify
import google.generativeai as genai
import vonage

# ---------------- HARD-CODED CONFIG ----------------
GENIE_API_KEY = "AIzaSyB0hthTJPT8XadaB7GkA3w0Gy5QKPyLVm4"
VONAGE_API_KEY = "9e21dc3a"
VONAGE_API_SECRET = "cttBO%SJicxArD$sd5GlBI*5"
WHATSAPP_NUMBER = "14157386102"     # Vonage sandbox number (example)
USER_NUMBER = "918660029082"        # Your WhatsApp number (with country code)

# ---------------- INITIALIZE ----------------
genai.configure(api_key=GENIE_API_KEY)
model = genai.GenerativeModel("models/gemini-2.0-flash")

vonage_client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
messaging = vonage.Messaging(vonage_client)

app = Flask(__name__)

# ---------------- FUNCTION: Answer GK Question ----------------
def gk_answer(question: str):
    prompt = f"You are a general knowledge assistant. Answer in one short and clear paragraph.\n\nQuestion: {question}"
    response = model.generate_content(prompt)
    return response.text.strip()

# ---------------- FUNCTION: Send WhatsApp ----------------
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

# ---------------- ROUTES ----------------
@app.route("/", methods=["GET"])
def home():
    return "✅ GK WhatsApp Chatbot is running."

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("Incoming webhook:", data)

    # Try to extract message text
    user_msg = None
    if isinstance(data, dict):
        user_msg = data.get("message", {}).get("content", {}).get("text")
    if not user_msg:
        user_msg = str(data)

    # Generate and send answer
    answer = gk_answer(user_msg)
    send_whatsapp(answer)
    return jsonify({"status": "ok", "question": user_msg, "answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
