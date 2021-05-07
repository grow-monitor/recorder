from src.config import (
    FAUNA_COLLECTION,
    FAUNA_SECRET,
    MQTT_HOST,
    MQTT_PASSWORD,
    MQTT_PORT,
    MQTT_USERNAME,
    TOPICS,
)
from src.record import Recorder


def run():
    recorder = Recorder(
        FAUNA_SECRET,
        FAUNA_COLLECTION,
        username=MQTT_USERNAME,
        password=MQTT_PASSWORD,
        host=MQTT_HOST,
        port=MQTT_PORT,
    )
    recorder.subscribe([(topic, 2) for topic in TOPICS])
    while True:
        recorder.run()


if __name__ == "__main__":
    run()
