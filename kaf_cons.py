import time
import json
from json import dumps
import pandas as pd
# from kafka import *
from confluent_kafka import Consumer
from pandas import DataFrame
from datetime import datetime
from time import sleep
import matplotlib.pyplot as plt

# brokers='localhost:9092'
# topic='stock'
# sleep_time=300
# offset='latest'

class ExampleConsumer:
    broker = "localhost:9092"
    topic = "stock"
    group_id = "consumer-1"

    def start_listener(self):
        consumer_config = {
            'bootstrap.servers': self.broker,
            'group.id': self.group_id,
            'auto.offset.reset': 'largest',
            'enable.auto.commit': 'false',
            'max.poll.interval.ms': '86400000'
        }

        consumer = Consumer(consumer_config)
        consumer.subscribe([self.topic])

        try:
            while True:
                print("Listening")
                # read single message at a time
                msg = consumer.poll(0)

                if msg is None:
                    sleep(5)
                    continue
                if msg.error():
                    print("Error reading message : {}".format(msg.error()))
                    continue
                # You can parse message and save to data base here
                resp = msg.value()
                resp = resp.decode("utf-8")
                loaded = json.loads(resp)
                temp = pd.read_json(loaded)
                # print(temp)
                df = pd.DataFrame()
                if 'name' in temp.columns:
                    df = df.append(temp, ignore_index=True)
                    name = temp['name'].values[0]
                    if name == 'apple':
                        df.to_csv('./AAPL_NEW.csv', sep = ',', index=False, header = False, mode='a')
                    elif name == 'microsoft': 
                        df.to_csv('./MSFT_NEW.csv', sep = ',', index=False, header = False, mode='a')
                    elif name == 'amazon':
                        df.to_csv('./AMZN_NEW.csv', sep = ',', index=False, header = False, mode='a')
                    elif name == 'facebook':
                        df.to_csv('./FB_NEW.csv', sep = ',', index=False, header = False, mode='a')
                    elif name == 'tesla':
                        df.to_csv('./TSLA_NEW.csv', sep = ',', index=False, header = False, mode='a')

                consumer.commit()

        except Exception as ex:
            print("Kafka Exception : {}", ex)

        finally:
            print("closing consumer")
            consumer.close()

#RUNNING CONSUMER FOR READING MESSAGE FROM THE KAFKA TOPIC
my_consumer = ExampleConsumer()
# df = pd.DataFrame()
# my_consumer.start_listener(df)
my_consumer.start_listener()


# conf = {'bootstrap.servers': "localhost:9092",
#         'group.id': "foo",
#         'auto.offset.reset': 'smallest'}

# consumer = Consumer(conf)

# # consumer = KafkaConsumer(bootstrap_servers=brokers, auto_offset_reset=offset,consumer_timeout_ms=1000)
# # consumer.subscribe([topic])
# consumer.subscribe([topic])

# try:
#     while True:
#         print("Listening")
#         # read single message at a time
#         msg = consumer.poll(0)

#         if msg is None:
#             sleep(5)
#             continue
#         if msg.error():
#             print("Error reading message : {}".format(msg.error()))
#             continue
#         # You can parse message and save to data base here
#         print(msg)
#         consumer.commit()

# except Exception as ex:
#     print("Kafka Exception : {}", ex)

# finally:
#     print("closing consumer")
#     consumer.close()

# # while(True):
# #     for message in consumer:
# #         #print(message)
# #         d=json.loads(message.value)
# #         df=DataFrame(d)
# #         print(df)
        
# #     time.sleep(sleep_time)