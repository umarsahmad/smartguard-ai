import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883

def create_client():
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)
    return client

def publish(topic, message):
    client = create_client()
    client.loop_start()
    client.publish(topic, message)
    client.loop_stop()
