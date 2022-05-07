import db
import datetime
import paho.mqtt.client as paho
from paho import mqtt
from db import DBPATH

counter = 0

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"<SERVER> CONNACK received with code {rc}.")

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print(f"<SERVER> Subscribed: {str(mid)}, QOS: {str(granted_qos[0])}")

def on_message(client, userdata, msg):
    global counter
    print(f"[{counter}] <SERVER> Message from topic {msg.topic}, qos {msg.qos}, text {str(msg.payload)}")
    counter += 1
    device = msg.topic.split("/")[1]
    if device not in device_time:
        device_time[device] = datetime.datetime.now()
    temp = float(msg.payload.decode("utf-8"))
    time = device_time[device]
    db.add_temp(dbcon, device, temp, time)
    device_time[device] += datetime.timedelta(minutes=10)

device_time = {}

# setting db
dbcon = db.create_connection(DBPATH)
db.create_temp_table(dbcon)

# create mqtt client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("mqttC", "PzX2nUnfVyt5TEG")
client.connect("5295f809b44f4def8eecc6af6fd365c3.s2.eu.hivemq.cloud", 8883)

client.on_subscribe = on_subscribe
client.on_message = on_message
client.subscribe("temperature/#", qos=2)
client.loop_forever()
dbcon.close()