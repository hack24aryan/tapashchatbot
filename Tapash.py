from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os

# Initialize Flask App
app = Flask(__name__)

# Route for the home page (Root URL)
@app.route('/')
def home():
    return "Hello, World!"  # Or your desired home page content

if __name__ == '__main__':
    app.run(debug=True)

# Set OpenAI API Key (replace with your key or set it as an environment variable)
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Function to Generate ChatGPT Responses
def generate_answer(question):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",  # Use GPT-4 if you have access
            prompt=f"Q: {question}\nA:",
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return "Sorry, something went wrong. Please try again later."

# Route for WhatsApp Messages
@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").strip()
    print(f"Received: {incoming_msg}")
    answer = generate_answer(incoming_msg)
    print(f"Reply: {answer}")
    resp = MessagingResponse()
    resp.message(answer)
    return str(resp)

# Run the Flask App Locally
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
