import vonage
import google.generativeai as genai

# =========================
# 1️⃣ Hardcoded API Keys
# =========================
VONAGE_API_KEY = "9e21dc3a"
VONAGE_API_SECRET = "cttBO%SJicxArD$sd5GlBI*5"
VONAGE_WHATSAPP_NUMBER = "14157386102"
TO_WHATSAPP_NUMBER = "918660029082"  # Recipient number

GOOGLE_API_KEY = "AIzaSyB0hthTJPT8XadaB7GkA3w0Gy5QKPyLVm4"

# =========================
# 2️⃣ Initialize Clients
# =========================
# Vonage Messages client (direct API key/secret)
messages = vonage.Messages(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)

# Google Generative AI
genai.configure(api_key=GOOGLE_API_KEY)

# =========================
# 3️⃣ Generate AI Response
# =========================
def get_ai_response(prompt):
    """Generate response from Google Generative AI"""
    response = genai.chat.completions.create(
        model="chat-bison-001",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message["content"]

# =========================
# 4️⃣ Send WhatsApp Message
# =========================
def send_whatsapp_message(to_number, text):
    response = messages.send_message({
        "from": {"type": "whatsapp", "number": VONAGE_WHATSAPP_NUMBER},
        "to": {"type": "whatsapp", "number": to_number},
        "message": {"content": {"type": "text", "text": text}}
    })
    return response

# =========================
# 5️⃣ Main Function
# =========================
if __name__ == "__main__":
    user_input = input("Enter your message for AI: ")
    
    # Generate AI response
    ai_text = get_ai_response(user_input)
    print("AI says:", ai_text)
    
    # Send AI response via WhatsApp
    whatsapp_response = send_whatsapp_message(TO_WHATSAPP_NUMBER, ai_text)
    print("WhatsApp API Response:", whatsapp_response)
