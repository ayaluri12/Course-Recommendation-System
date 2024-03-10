import sys
import time
import json
from json import dumps
# from kafka import KafkaProducer
from confluent_kafka import Producer
from time import sleep
import requests as req
import yfinance as yf

from dataload import uploadData,downloadData,getCollections

# brokers='localhost:9092'
# topic='stock'
# sleep_time=300

class ExampleProducer:
    broker = "localhost:9092"
    topic = "stock"
    producer = None

    def __init__(self):
        self.producer = Producer({
            'bootstrap.servers': self.broker,
            'socket.timeout.ms': 100,
            'api.version.request': 'false',
            'broker.version.fallback': '0.9.0',
        }
        )

    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(
                msg.topic(), msg.partition()))

    def send_msg_async(self, msg):
        print("Send message asynchronously")
        self.producer.produce(
            self.topic,
            msg,
            callback=lambda err, original_msg=msg: self.delivery_report(err, original_msg
                                                                        ),
        )
        self.producer.flush()

    def send_msg_sync(self, msg):
        print("Send message synchronously")
        self.producer.produce(
            self.topic,
            msg,
            callback=lambda err, original_msg=msg: self.delivery_report(
                err, original_msg
            ),
        )
        self.producer.flush()


#SENDING DATA TO KAFKA TOPIC
example_producer = ExampleProducer()
while True:
    resp_ap = yf.download('AAPL', period='1m', interval='1m')
    resp_ap['name']='apple'
    json_data_ap = resp_ap.to_json(orient='records')
    example_producer.send_msg_async(dumps(json_data_ap))

    resp_msft = yf.download('MSFT', period='1m', interval='1m')
    resp_msft['name']='microsoft'
    json_data_m = resp_msft.to_json(orient='records')
    example_producer.send_msg_async(dumps(json_data_m))


    resp_amz = yf.download('AMZN', period='1m', interval='1m')
    resp_amz['name']='amazon'
    json_data_amz = resp_amz.to_json(orient='records')
    example_producer.send_msg_async(dumps(json_data_amz))

    resp_fb = yf.download('FB', period='1m', interval='1m')
    resp_fb['name']='facebook'
    json_data_fb = resp_fb.to_json(orient='records')
    example_producer.send_msg_async(dumps(json_data_fb))

    resp_tl = yf.download('TSLA', period='1m', interval='1m')
    resp_tl['name']='tesla'
    json_data_tl = resp_tl.to_json(orient='records')
    example_producer.send_msg_async(dumps(json_data_tl))
    time.sleep(30)
# conf = {'bootstrap.servers': "localhost:9092"}

# producer = Producer(conf)

# # producer = Producer(bootstrap_servers=[brokers],value_serializer=lambda x: dumps(x).encode('utf-8'))

# while(True):
#     print("Getting new data...")
#     resp = yf.download('AAPL', period='1m', interval='1m')
#     json_data = resp.to_json(orient='records')
#     producer.produce(topic, key="key", value=dumps(json_data))
#     # producer.send(topic, json_data)
#     time.sleep(sleep_time)