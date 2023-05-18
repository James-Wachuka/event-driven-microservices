from flask import Flask, jsonify, request
import psycopg2
from kafka import KafkaProducer
import json

app = Flask(__name__)

# Database connection configuration
db_host = 'localhost'
db_port = 5432
db_name = 'kafka'
db_user = 'data_eng'
db_password = 'data_eng'

# Kafka producer configuration
bootstrap_servers = 'localhost:9092'
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Create a connection to the database
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_password
)

# API endpoint to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    try:
        # Extract user information from the request
        user_data = request.get_json()
        id = int(user_data['id'])
        name = user_data['name']

        # Insert the new user into the database
        cursor = conn.cursor()
        query = f"INSERT INTO users (id, name) VALUES ({id}, '{name}') RETURNING id"
        cursor.execute(query)
        conn.commit()

        # Publish user_created event to Kafka
        event_data = {'id': id, 'name': name}
        producer.send('user_created', value=event_data)

        return jsonify({'id':id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to get user information
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        # Retrieve user information from the database
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE id = {user_id}"
        cursor.execute(query)
        user = cursor.fetchone()

        if user:
            # Return user information as JSON
            return jsonify({
                'id': user[0],
                'name': user[1]
            })
        else:
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

# API endpoint to delete a user
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        # Delete the user from the database
        cursor = conn.cursor()
        query = f"DELETE FROM users WHERE id = {user_id}"
        cursor.execute(query)
        conn.commit()

        return jsonify({'message': 'User deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()