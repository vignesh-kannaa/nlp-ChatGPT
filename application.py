from flask import Flask, request, jsonify
import openai
import json

openai.api_key = "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"

app = Flask(__name__)


# Load conversation data from JSON file
with open('training-conversation.json', 'r') as json_file:
    conversation_data = json.load(json_file)

messages = []
for message in conversation_data:
    messages.append(message)

print(messages)


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    userText = data.get('msg')
    if userText:
        messages.append({"role": "user", "content": userText})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        ChatGPT_reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": ChatGPT_reply})
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
