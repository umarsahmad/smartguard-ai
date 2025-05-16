import time
from paho.mqtt.client import Client

MQTT_BROKER_HOST = "mosquitto"
MQTT_BROKER_PORT = 1883
TEST_TOPIC = "test/topic"
TEST_MESSAGE = "yo test passed"

def test_mqtt_publish_subscribe():
    received_messages = []
    connected_flag = False

    def on_connect(client, userdata, flags, rc):
        nonlocal connected_flag
        if rc == 0:
            connected_flag = True
            print("✅ Connected to broker")
        else:
            print(f"❌ Failed to connect: {rc}")

    def on_message(client, userdata, msg):
        decoded = msg.payload.decode()
        print(f"📩 Received message: {decoded}")
        received_messages.append(decoded)

    mqtt_client = Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
    mqtt_client.loop_start()

    # Wait for connection
    timeout = 5
    start = time.time()
    while not connected_flag and time.time() - start < timeout:
        time.sleep(0.1)

    assert connected_flag, "Failed to connect to MQTT broker"

    mqtt_client.subscribe(TEST_TOPIC)
    time.sleep(1)  # Wait for subscription

    mqtt_client.publish(TEST_TOPIC, TEST_MESSAGE)

    # Wait for message
    start = time.time()
    while time.time() - start < timeout:
        if TEST_MESSAGE in received_messages:
            break
        time.sleep(0.1)

    mqtt_client.loop_stop()

    assert TEST_MESSAGE in received_messages, f"Expected '{TEST_MESSAGE}', got {received_messages}"
