import pytest
import time
import subprocess
import paho.mqtt.client as mqtt

@pytest.fixture(scope="session")
def start_mqtt_broker():
    process = subprocess.Popen(['mosquitto', '-p', '1883'])
    time.sleep(2)
    yield
    process.terminate()

# Optional: sleep to let Docker broker warm up
@pytest.fixture(scope="module")
def mqtt_client():
    time.sleep(1)  # Let Docker broker fully start
    client = mqtt.Client()
    client.connect("mosquitto", 1883)
    return client
