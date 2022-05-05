import datetime
from mimetypes import init
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

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print(f"Subscribed: {str(mid)}, QOS: {str(granted_qos[0])}")

def on_message(client, userdata, msg):
    global device_name, ventilation
    temp = float(msg.payload.decode("utf-8"))
    if temp > 0:
        ventilation = True
    else:
        ventilation = False
    generate_temp(client, device_name, temp)

def generate_temp(client, device_name, current_temp=None):
    global ventilation
    tp = change_time_temp(datetime.datetime.now().hour) if not ventilation else current_temp
    temp = round(gauss(tp, 0.2), 1)
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
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("epmqttuser", "P4ssw0rd123987!")
client.connect("e0bbb35ea4f34a6abdc1e48aec812392.s2.eu.hivemq.cloud", 8883)
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_message = on_message
client.subscribe(f"{device_name}/temp", qos=1)
ventilation = False

current_temp = init_temp
while True:
    current_temp = generate_temp(client, device_name, current_temp)
    print(current_temp)
    time.sleep(pub_rate)