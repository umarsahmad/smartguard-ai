import pytest
import time
from paho.mqtt.client import Client

TEST_TOPIC = "test/topic"
TEST_MESSAGE = "yo test passed"

@pytest.fixture(scope="module")
def mqtt_client():
    client = Client()
    client.connect("localhost", 1883)
    return client

def test_mqtt_publish_subscribe(mqtt_client):
    received_messages = []

    def on_message(client, userdata, msg):
        print(f"📩 Received: {msg.payload.decode()}")
        received_messages.append(msg.payload.decode())

    mqtt_client.subscribe(TEST_TOPIC)
    mqtt_client.on_message = on_message
    mqtt_client.loop_start()

    # Wait for subscription to register on broker
    time.sleep(1)

    mqtt_client.publish(TEST_TOPIC, TEST_MESSAGE)

    # Give it a moment to receive the message
    timeout = 5
    for _ in range(timeout * 10):  # check for 5s total
        if received_messages:
            break
        time.sleep(0.1)

    mqtt_client.loop_stop()

    assert TEST_MESSAGE in received_messages, f"Expected '{TEST_MESSAGE}', got {received_messages}"
