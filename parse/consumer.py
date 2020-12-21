import json
from kafka import KafkaConsumer
kafka_host_1 = '172.16.30.25'
kafka_host_2 = '172.16.30.45'
kafka_host_3 = '172.16.30.65'


consumer = KafkaConsumer('logger',value_deserializer=json.loads,
                         bootstrap_servers=['{}:9092'.format(kafka_host_1),'{}:9092'.format(kafka_host_2),'{}:9092'.format(kafka_host_3)]
                         )
for u in consumer:
    print(u.value)