import json
from typing import List, Literal, Optional, Tuple

import paho.mqtt.client as mqtt
from faunadb import query as q
from faunadb.client import FaunaClient

from src.types import Data, QoS, QueryResult


class Recorder(object):
    """
    Subscribes to data from an MQTT broker and records it to the "soil" collection in the given FaunaDB instance.
    Assumes that an index "data_by_topic", which allows documents to be searched by their topic, has been created
    under the soil collection.
    """

    def __init__(
        self,
        secret: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        host: str = "test.mosquitto.org",
        port: int = 8883,
        client_id: Optional[str] = None,
    ):
        """
        Parameters
        ----------
        secret : str
            Auth token for the FaunaDB server.
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
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
        self.client.username_pw_set(username, password=password)
        self.client.connect(host, port=port)
        self.db = FaunaClient(secret=secret)

    @property
    def collection(self):
        return q.collection("soil")

    @property
    def index(self):
        return q.index("data_by_topic")

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully")
        else:
            print("Connect returned result code: {}".format(rc))

    def _on_message(self, client, userdata, msg: mqtt.MQTTMessage):
        data = self._parse(msg)
        self.record(data)

    def _parse(self, msg: mqtt.MQTTMessage) -> Data:
        payload: dict = json.loads(msg.payload)
        payload.update({"topic": msg.topic, "timestamp": q.time(payload["timestamp"])})
        return payload

    def subscribe(self, topics: List[Tuple[str, QoS]]):
        """Subscribes to the MQTT broker for the given topics.

        Parameters
        ----------
        topics : List[Tuple[str, QoS]]
            List of topics to subscribe to, along with the desired quality of service (QoS).
        """
        self.client.subscribe(topics)

    def record(self, data: Data) -> QueryResult:
        """In one query, updates existing topic document with data 
           if document already exists, else create a new document.

        Parameters
        ----------
        data : Data
            Parsed message from the MQTT broker.

        Returns
        -------
        QueryResult
            See src.types.QueryResult for its signature.
        """
        topic = q.match(self.index, data.get("topic", ""))
        update_record = q.update(q.select(["ref"], q.get(topic)), {"data": data})
        create_record = q.create(self.collection, {"data": data})
        result = self.db.query(
            q.let(
                {"topic_exists": q.exists(topic)},
                q.if_(q.var("topic_exists"), update_record, create_record),
            )
        )
        return result

    def run(self):
        self.client.loop()

