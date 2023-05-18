from kafka import KafkaAdminClient
from kafka.admin import NewTopic


# Kafka admin configuration
bootstrap_servers = 'localhost:9092'
admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

# Create Kafka topics
topics = [
    NewTopic(name='user_created', num_partitions=1, replication_factor=1),
    NewTopic(name='order_placed', num_partitions=1, replication_factor=1)
]
admin_client.create_topics(new_topics=topics)
