import os
from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Initialize the OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Define a function to generate answers using GPT-3
def generate_answer(question):
    model_engine = "text-davinci-002"
    prompt = (f"Q: {question}\n"
              "A:")

   response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # Use "gpt-4" if needed
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Your question"}
    ],
    max_tokens=100,
    temperature=0.7
)

    answer = response.choices[0].text.strip()
    return answer


# Route for the home page (Root URL)
@app.route('/')
def home():
    return "Hello, World!"  # Or your desired home page content

# Route to handle incoming WhatsApp messages
@app.route('/chatgpt', methods=['POST'])
def chatgpt():
    incoming_que = request.values.get('Body', '').lower()
    print("Question: ", incoming_que)

    # Generate the answer using GPT-3
    answer = generate_answer(incoming_que)
    print("BOT Answer: ", answer)

    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    msg.body(answer)
    return str(bot_resp)

if __name__ == '__main__':
    # Use the port that Render provides or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
