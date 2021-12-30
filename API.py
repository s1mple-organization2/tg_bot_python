from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def hello():
    return "<p>Flask app work!</p>"


@app.route('/api/order', methods=['POST'])
def get_Order_Data():
    request_data = request.get_json()
    # id = request_data['id']
    print(request_data)
    return request_data


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)
