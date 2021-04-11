import paho.mqtt.client as mqtt
import psycopg2
from pgcopy import CopyManager

import config


class Recorder(object):
    def __init__(self, username, password, host, port):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
        self.client.username_pw_set(username, password)
        self.client.connect(host, port)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully")
        else:
            print("Connect returned result code: {}".format(rc))

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        qos = msg.qos.decode("utf-8")
        print(f"Received message {topic} -> {payload} with QoS {qos}")

    def subscribe(self, topics):
        result, message_id = self.client.subscribe(topics)
        return result, message_id

    def run(self):
        self.client.loop()


if __name__ == "__main__":
    recorder = Recorder(config.USERNAME, config.PASSWORD, config.HOST, config.PORT)
    recorder.subscribe([("mock/moisture", 2), ("mock/saturation", 2)])
    while True:
        recorder.run()


# with psycopg2.connect(config.DB_URL) as conn:
#     SQL = """
#     SELECT  generate_series(now() - interval '24 hour', now(), interval '5 minute') AS timestamp,
#     %s as topic,
#     random() AS value
#     """
#     cur = conn.cursor()
#     for topic in ("mock/saturation", "mock/moisture"):
#         data = (topic,)
#         cur.execute(SQL, data)
#         values = cur.fetchall()
#         print(values)

