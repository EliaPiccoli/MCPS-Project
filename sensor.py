import datetime
from mimetypes import init
import sys
import random
import time
import db
import paho.mqtt.client as paho
from _socket import herror
from paho import mqtt
from random import gauss, seed
from utilityFunction import change_time_temp
from db import DBPATH

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"CONNACK received with code {rc}")
    else:
        print(f"Failed connection to broker with code {rc}")
        exit()

def on_publish(client, userdata, mid, properties=None):
    global ventilation
    print(f"Ventilation: {ventilation}")

def generate_temp(client, device_name, hour):
    global ventilation, last_vent_temp
    tp = change_time_temp(hour, device_name) if not ventilation else last_vent_temp
    dev = 0.2 if not ventilation else 0
    print(hour, hour, tp, dev, client)
    temp = round(gauss(tp, dev), 1)
    client.publish(f"temperature/{device_name}", payload=temp, qos=1)
    client.loop(2, 10)
    return temp

seed(random.random())
if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <device_name> <pub_rate>")
    exit()
device_name = sys.argv[1]
pub_rate = float(sys.argv[2])
dbcon = db.create_connection(DBPATH)
client = paho.Client(client_id=device_name, userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS_CLIENT)
client.username_pw_set("mqttC", "PzX2nUnfVyt5TEG")
client.connect("5295f809b44f4def8eecc6af6fd365c3.s2.eu.hivemq.cloud", 8883)
client.on_publish = on_publish
ventilation = False
last_vent_temp = 0

current_time = datetime.datetime.now()
while True:
    v = db.get_device_vent(dbcon, device_name)
    if v is None or len(v) == 0:
        ventilation = False
    else:
        ventilation = True
        last_vent_temp = v[0][0]
    current_temp = generate_temp(client, device_name, current_time.hour)
    current_time += datetime.timedelta(minutes=10)
    print(f"{device_name} - Temperature: {current_temp}")
    time.sleep(pub_rate)
