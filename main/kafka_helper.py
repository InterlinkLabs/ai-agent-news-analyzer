from constant import KAFKA_SERVER, CONSUME_TOPIC
"""
This module provides helper functions for interacting with Kafka, including creating Kafka consumers and a producer.

Constants:
  KAFKA_SERVER (str): The address of the Kafka server.
  CONSUME_TOPIC (dict): A dictionary containing the topics to consume from.

Kafka Consumers:
  consumer_audio (KafkaConsumer): A Kafka consumer for the 'audio' topic.
  consumer_video (KafkaConsumer): A Kafka consumer for the 'video' topic.
  consumer_document (KafkaConsumer): A Kafka consumer for the 'document' topic.

Kafka Producer:
  producer (KafkaProducer): A Kafka producer for publishing messages to Kafka topics.
"""
from kafka import KafkaConsumer, KafkaProducer
import json

# Create kafka consummer
consumer_audio = KafkaConsumer(
  CONSUME_TOPIC['audio'],
  bootstrap_servers=[KAFKA_SERVER],
  group_id="demo-group",
  auto_offset_reset="earliest",
  enable_auto_commit=False,
  consumer_timeout_ms=1000
)

consumer_video = KafkaConsumer(
  CONSUME_TOPIC['video'],
  bootstrap_servers=[KAFKA_SERVER],
  group_id="demo-group",
  auto_offset_reset="earliest",
  enable_auto_commit=False,
  consumer_timeout_ms=1000
)

consumer_document = KafkaConsumer(
  CONSUME_TOPIC['document'],
  bootstrap_servers=[KAFKA_SERVER],
  group_id="demo-group",
  auto_offset_reset="earliest",
  enable_auto_commit=False,
  consumer_timeout_ms=1000
)

# Create kafka publisher
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,  # Replace with your Kafka broker address
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize messages as JSON
)