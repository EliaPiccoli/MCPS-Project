import datetime
from mimetypes import init
import sys
import random
import time
import paho.mqtt.client as paho
from _socket import herror
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
    # print(f"Client {str(client)} published message {mid}")
    global ventilation
    print(f"Ventilation: {ventilation}")


def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print(f"Subscribed: {str(mid)}, QOS: {str(granted_qos[0])}")


def on_message(client, userdata, msg):
    global device_name, ventilation, last_vent_temp
    print(f"########### {device_name} received message ###########")
    temp = float(msg.payload.decode("utf-8"))
    if temp > 0:
        ventilation = True
        last_vent_temp = temp
    else:
        ventilation = False
    generate_temp(client, device_name, -1, temp)  # add time correct

def generate_temp(client, device_name, hour, current_temp=None):
    global ventilation, current_time, last_vent_temp
    if hour < 0:
        h = (current_time + datetime.timedelta(minutes=15)).hour
    else:
        h = hour
    tp = change_time_temp(h, device_name) if not ventilation else last_vent_temp
    dev = 0.2 if not ventilation else 0
    print(hour, h, tp, dev, client)
    # if tp is None:
    #     tp = change_time_temp(hour, device_name)
    temp = round(gauss(tp, dev), 1)
    client.publish(f"temperature/{device_name}", payload=temp, qos=1)

    if hour >= 0:       # main loop
        client.loop(2, 10)
    else:               # vent
        client.loop_start()

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
client.on_subscribe = on_subscribe
client.on_message = on_message
client.subscribe(f"{device_name}/temp", qos=1)
ventilation = False
last_vent_temp = 0

current_temp = init_temp
current_time = datetime.datetime.now()

time_current = datetime.datetime.now()
while True:
    current_temp = generate_temp(client, device_name, current_time.hour, current_temp)
    current_time += datetime.timedelta(minutes=15)
    print(f"{device_name} - Temperature: {current_temp}")
    time.sleep(pub_rate)
