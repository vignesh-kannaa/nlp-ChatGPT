from flask import Flask, request, jsonify
import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is not None:
    print('api key added')

app = Flask(__name__)


# Load conversation data from JSON file
with open('training-conversation.json', 'r') as json_file:
    conversation_data = json.load(json_file)

messages = []
for message in conversation_data:
    messages.append(message)


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    userText = data.get('msg')
    if userText:
        messages.append({"role": "user", "content": userText})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=30
        )
        ChatGPT_reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "system", "content": ChatGPT_reply})
        return jsonify(ChatGPT_reply)

    # if 'messages' in data:
    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=data['messages']
    #     )
    #     return jsonify(response.choices[0].message['content'])

    return jsonify({"error": "Invalid input format."}), 400


if __name__ == '__main__':
    app.run()


# myenv\Scripts\activate
