from kafka import KafkaProducer
import requests
import json

# Kafka producer configuration
bootstrap_servers = 'localhost:9092'

# Webhook URLs
user_created_webhook = 'http://localhost:5000/webhook/user_created'
order_placed_webhook = 'http://localhost:5000/webhook/order_placed'

# Create Kafka producer
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Publish user created event
user = {'id': 11, 'name': 'King'}
producer.send('user_created', value=user)

# Send webhook notification for user created event
requests.post(user_created_webhook, json=user)

# Publish order placed event
order = {'id': 11, 'product': 'sofa', 'amount': 100000}
producer.send('order_placed', value=order)

# Send webhook notification for order placed event
requests.post(order_placed_webhook, json=order)

# Close the producer connection
producer.close()
