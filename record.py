import json

import paho.mqtt.client as mqtt
import psycopg2

from config import DB_URL, HOST, PASSWORD, PORT, TABLE, USERNAME


class Recorder(object):
    def __init__(self, username, password, host, port):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
        self.client.username_pw_set(username, password)
        self.client.connect(host, port)
        self.conn = psycopg2.connect(DB_URL)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully")
        else:
            print("Connect returned result code: {}".format(rc))

    def on_message(self, client, userdata, msg):
        data = self.parse(msg)
        self.insert(data)

    def parse(self, msg):
        topic = msg.topic.split("/")[-1]
        payload = json.loads(msg.payload)
        return (payload["timestamp"], topic, payload["value"])

    def subscribe(self, topics):
        result, message_id = self.client.subscribe(topics)
        return result, message_id

    def insert(self, data):
        cur = self.conn.cursor()
        query = f"INSERT INTO {TABLE} (timestamp, topic, value) VALUES (?, ?, ?);"
        try:
            cur.execute(query, data)
        except (Exception, psycopg2.Exception) as err:
            print(f"Unable to insert data: {err}")
        self.conn.commit()

    def run(self):
        self.client.loop()


if __name__ == "__main__":
    recorder = Recorder(USERNAME, PASSWORD, HOST, PORT)
    recorder.subscribe([("mock/moisture", 2), ("mock/saturation", 2)])
    while True:
        recorder.run()

