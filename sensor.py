import datetime
import sys
import random
import time
import paho.mqtt.client as paho
from paho import mqtt
from random import gauss, seed
from utilityFunction import change_time_temp

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"CONNACK received with code {rc}")
    else:
        print(f"Failed connection to broker with code {rc}")
        exit()

def on_publish(client, userdata, mid, properties=None):
    print(f"Client {str(client)} published message {mid}")


def generate_temp(current_temp, client, device_name):
    temp = round(gauss(change_time_temp(datetime.datetime.now().hour, device_name), 0.2), 1)
    client.publish(f"temperature/{device_name}", payload=temp, qos=1)
    client.loop(2, 10)
    return temp

seed(random.random())
if len(sys.argv) < 4:
    print(f"Usage: {sys.argv[0]} <device_name> <init_temp> <pub_rate>")
    exit()
device_name = sys.argv[1]
init_temp = float(sys.argv[2])
pub_rate = int(sys.argv[3])

client = paho.Client(client_id=device_name, userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS_CLIENT)
client.username_pw_set("mqttC", "PzX2nUnfVyt5TEG")
client.connect("5295f809b44f4def8eecc6af6fd365c3.s2.eu.hivemq.cloud", 8883)
client.on_publish = on_publish

while True:
    current_temp = generate_temp(init_temp, client, device_name)
    print(current_temp)
    time.sleep(pub_rate)


