from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook/user_created', methods=['POST'])
def handle_user_created_webhook():
    payload = request.get_json()
    # Perform necessary actions or trigger other processes based on the user created event
    print('New user created:', payload)
    # ...
    return 'Webhook received and processed successfully', 200

@app.route('/webhook/order_placed', methods=['POST'])
def handle_order_placed_webhook():
    payload = request.get_json()
    # Perform necessary actions or trigger other processes based on the order placed event
    print('New order placed:', payload)
    # ...
    return 'Webhook received and processed successfully', 200

if __name__ == '__main__':
    app.run()
