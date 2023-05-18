from kafka import KafkaConsumer
import json
import psycopg2

# Database connection configuration
db_host = 'localhost'
db_port = 5432
db_name = 'kafka'
db_user = 'data_eng'
db_password = 'data_eng'

# Create a connection to the database
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_password
)

# Kafka consumer configuration
bootstrap_servers = 'localhost:9092'

# Create Kafka consumer for user_created events
user_consumer = KafkaConsumer('user_created',
                              bootstrap_servers=bootstrap_servers,
                              group_id='user_consumer_group',
                              value_deserializer=lambda v: json.loads(v.decode('utf-8')))

# Create Kafka consumer for order_placed events
order_consumer = KafkaConsumer('order_placed',
                               bootstrap_servers=bootstrap_servers,
                               group_id='order_consumer_group',
                               value_deserializer=lambda v: json.loads(v.decode('utf-8')))

#create table for users and orders
cursor = conn.cursor()
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id INT,
    name VARCHAR(100) NOT NULL
)
"""
cursor.execute(create_users_table)



create_orders_table = """
CREATE TABLE IF NOT EXISTS orders (
    id INT,
    product VARCHAR(100) NOT NULL,
    amount INT
)
"""
cursor.execute(create_orders_table)
conn.commit()
cursor.close()

# Consume user_created and order_placed events
for message_1, message_2 in zip(user_consumer,order_consumer):

    user = message_1.value
    order = message_2.value

    cursor = conn.cursor()
    # Insert user data into the database
    user_query = f"INSERT INTO users (id, name) VALUES ({user['id']}, '{user['name']}')"
    order_query = f"INSERT INTO orders (id, product, amount) VALUES ({order['id']}, '{order['product']}', {order['amount']})"

    cursor.execute(user_query)
    print('New user created:', user)
    cursor.execute(order_query)
    print('New order placed:', order)


    conn.commit()
    cursor.close()


# Close the database connection
conn.close()
