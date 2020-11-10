# -*- coding: utf-8 -*-
import json
from kafka import KafkaProducer
from kafka import KafkaConsumer
kafka_host_1 = '172.16.30.25'
kafka_host_2 = '172.16.30.45'
kafka_host_3 = '172.16.30.65'

producer = KafkaProducer(
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    bootstrap_servers=['{}:9092'.format(kafka_host_1),'{}:9092'.format(kafka_host_2),'{}:9092'.format(kafka_host_3)]
)

producer.send(topic='logger',value='200')
producer.close()

