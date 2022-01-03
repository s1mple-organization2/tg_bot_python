import requests
import config
from flask import Flask, request

app = Flask(__name__)


def send_message(chat_id, text):
    method = "sendMessage"
    url = f"https://api.telegram.org/bot{config.TOKEN}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


@app.route("/")
def hello():
    return "<p>Flask app work!</p>"


# Тестовый запрос пример http://192.168.0.105:5000/send?id=379085521
@app.route("/send", methods=['GET'])
def send():
    chat_id = request.args.get('id')
    text = request.args.get('text')
    send_message(chat_id, text)
    return "<p> Message from " + chat_id + " sent</p>"


@app.route('/api/order', methods=['POST'])
def get_Order_Data():
    request_data = request.get_json()
    # id = request_data['id']
    print(request_data)
    return request_data

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)
