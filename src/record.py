import json
from typing import List, Literal, Optional, Tuple

import paho.mqtt.client as mqtt
from faunadb import query as q
from faunadb.client import FaunaClient

from src.types import QoS, QueryResult


class Recorder(object):
    """
    Subscribes to data from an MQTT broker and records it to a FaunaDB instance.
    """

    def __init__(
        self,
        secret: str,
        collection_name: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        host: str = "test.mosquitto.org",
        port: int = 8883,
        client_id: Optional[str] = None,
    ) -> None:
        """
        Parameters
        ----------
        secret : str
            Auth token for the FaunaDB server.
        collection_name : str
            Name of the collection (table) in FaunaDB to record data to.
        username : Optional[str], optional
            The username to authenticate to the MQTT broker with.
            Set to None if not using username/password for broker authentication.
        password : Optional[str], optional
            The password to authenticate to the MQTT broker with.
            Set to None if not using password-based authentication.
        host : str, optional
            Host name or IP address of the remote broker, by default "test.mosquitto.org".
        port : int, optional
            Network port of the MQTT broker to connect to, by default 8883.
        client_id : Optional[str], optional
            The unique client id string used when connecting to the broker.
            If it has zero length or is None, then one will be randomly generated.
        """
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
        self.client.username_pw_set(username, password=password)
        self.client.connect(host, port=port)
        self.db = FaunaClient(secret=secret)
        self.collection = self.db.query(q.collection(collection_name))

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully")
        else:
            print("Connect returned result code: {}".format(rc))

    def on_message(self, client, userdata, msg: mqtt.MQTTMessage):
        data = self.parse(msg)
        self.record(data)

    def parse(self, msg: mqtt.MQTTMessage) -> dict:
        payload: dict = json.loads(msg.payload)
        payload.update({"topic": msg.topic, "timestamp": q.time(payload["timestamp"])})
        return payload

    def subscribe(self, topics: List[Tuple[str, QoS]]):
        result, message_id = self.client.subscribe(topics)
        return result, message_id

    def record(self, data: dict) -> QueryResult:
        query_obj = q.create(self.collection, {"data": data})
        result = self.db.query(query_obj)
        return result

    def run(self):
        self.client.loop()

