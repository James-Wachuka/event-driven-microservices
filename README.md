# Event-Driven Microservices with Webhooks & database Integration

This project demonstrates an event-driven microservices architecture using Apache Kafka for event streaming and webhook integration with external services. The architecture allows for scalable and decoupled communication between microservices through events, and enables external services to receive notifications and interact with the microservices via webhooks. A shared database allows for microservices to store data.

## Features

- Publish and consume events using Apache Kafka.
- Implement microservices that react to specific events.
- Integrate with external services using webhooks.
- integrate with a database
- Handle event-driven workflows efficiently.

## Architecture

The architecture consists of the following components:

- **Apache Kafka**: A distributed event streaming platform for publishing and consuming events.
- **Microservices**: Independent services that react to specific events and perform relevant actions or processes.
- **Webhooks**: Mechanism for external services to receive notifications and interact with the microservices.
- **Database**: a shared postgres db for microservices to store data.
 

## Getting Started

### Prerequisites

- Apache Kafka (running locally or on a server)
- Python 3.x

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/James-Wachuka/event-driven-microservices.git
   ```

2. Install the required Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Usage

Start Apache Kafka and create the necessary topics.
   - code [create-topics.py](create-topics.py)
   
## Webhook Integration

The webhook integration enables external services to interact with the microservices by sending HTTP POST requests to the webhook endpoints.
Start your microservices(using webhooks):

   ```
   webhook_app.py
   producer_for_webhook.py
   ```

### Sending a Webhook Notification
To send a webhook notification, make an HTTP POST request to the webhook endpoint with the relevant payload in JSON format.

Example Request:

```
curl -X POST -H "Content-Type: application/json" -d '{"id":"8","name": "samuel"}' http://localhost:5000/user_created
```

### Handling the Webhook Notification
The webhook endpoint receives the HTTP POST request, extracts the payload, and triggers the specified actions or processes within the microservices.

Example Endpoint:

```python
@app.route('/webhook/user_created', methods=['POST'])
def handle_user_created_webhook():
    payload = request.get_json()
    # Perform necessary actions or trigger other processes based on the user created event
    print('New user created:', payload)
    # ...
    return 'Webhook received and processed successfully', 200
```
## useful commands

check topics

```
./kafka-3.4.0-src/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```
delete topics

```
./kafka-3.4.0-src/bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic my-topic
```

check messages for the topics

```
./kafka-3.4.0-src/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic user_created --from-beginning
./kafka-3.4.0-src/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic order_placed --from-beginning
```

### integrating with a database
create user in postgres
```sudo -u postgres psql```
```
CREATE USER data_eng WITH PASSWORD 'data_eng';
CREATE DATABASE kafka;
GRANT ALL PRIVILEGES ON DATABASE kafka TO data_eng;
```
## create a consumer to send data to db
code: [consumer_to_db.py](consumer_to_db.py)
start the microservices(to send data to shared database).The producer for webhooks sends messages which can also be consumed and sent to database.

```
webhook_app.py
producer_for_webhook.py
consumer_to_db.py
```

### Performing CRUD operatioons on the shared database
Using [crud_app.py](crud_app.py) app we can perform CRUD operations on the shared database:
example endpoint:

```
# API endpoint to update user information
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        # Extract updated user information from the request
        user_data = request.get_json()
        name = user_data['name']

        # Update user information in the database
        cursor = conn.cursor()
        query = f"UPDATE users SET name = '{name}' WHERE id = {user_id}"
        cursor.execute(query)
        conn.commit()

        # Publish user_updated event to Kafka
        event_data = {'id': int(user_id), 'name': name}
        producer.send('user_updated', value=event_data)

        return jsonify({'message': 'User updated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


````

example of a request:

```
curl -X PUT -H "Content-Type: application/json" -d '{"name": "Elon"}' http://localhost:5000/users/8
``` 


## Contributing

Contributions are welcome!.

## License

This project is licensed under the [MIT License](LICENSE).


