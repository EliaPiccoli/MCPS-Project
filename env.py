import db
import time
import random
import paho.mqtt.client as paho
from paho import mqtt
from db import DBPATH

dbcon = db.create_connection(DBPATH)
MAX_VENT = 5
idx2dev = {}

def create_client():
    client = paho.Client(client_id="env", userdata=None, protocol=paho.MQTTv5)
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set("epmqttuser", "P4ssw0rd123987!")
    client.connect("e0bbb35ea4f34a6abdc1e48aec812392.s2.eu.hivemq.cloud", 8883)
    return client

def get_state(vent=None):
    global idx2dev
    ans = db.get_last_temp(dbcon)
    state = []
    for index, sens in enumerate(ans):
        state.append(sens[1])
        idx2dev[index] = sens[0]
    ventilation = random.randint(1, MAX_VENT) if vent is None else vent
    state.append(ventilation)
    return state

def step(state, action):
    next_state = []
    reward = 0.0

    hot_list = []
    cold_list = []
    if action == 0:             # from hottest to coldest
        temp = state[:-1]
        hot = max(temp)
        hot_index = temp.index(hot)
        cold = min(temp)
        cold_index = temp.index(cold)
        new_cold = cold + state[-1]/MAX_VENT
        new_hot = hot - state[-1]/MAX_VENT
        hot_list.append((hot_index, new_hot))
        cold_list.append((cold_index, new_cold))
    elif action == 1:           # from hottest to all
        temp = state[:-1]
        hot = max(temp)
        hot_index = temp.index(hot)
        new_hot = hot - state[-1]/MAX_VENT
        hot_list.append((hot_index, new_hot))
        for index, v in enumerate(temp):
            if index != hot_index:
                cold_list.append((index, v + state[-1]/MAX_VENT))
    elif action == 2:           # from hottest to temp < avg
        temp = state[:-1]
        hot = max(temp)
        hot_index = temp.index(hot)
        new_hot = hot - state[-1]/MAX_VENT
        hot_list.append((hot_index, new_hot))
        avg = sum(temp)/len(temp)
        for index, v in enumerate(temp):
            if v < avg:
                cold_list.append((index, v + state[-1]/MAX_VENT))

    # send to devices changes in temp
    client = create_client()
    for hot_index, new_hot in hot_list:
        client.publish(f"{idx2dev[hot_index]}/temp", payload=new_hot, qos=1)
        client.loop(60, 20)
    for cold_index, new_cold in cold_list:
        client.publish(f"{idx2dev[cold_index]}/temp", payload=new_cold, qos=1)
        client.loop(60, 20)
    client.disconnect()
    
    time.sleep(2)
    
    # read new temp
    next_state = get_state(state[-1])

    # generate reward
    avg = sum(next_state[:-1])/len(next_state[:-1])
    for t in next_state[:-1]:
        reward -= abs(t-avg)
    reward -= next_state[-1]*0.07*0.5

    # if equals -> done
    first = next_state[0]
    for t in next_state[:-1]:
        if abs(first - t) > 0.7:
            return next_state, reward, False
    return next_state, reward, True

def vent_off():
    client = create_client()
    for k in idx2dev:
        client.publish(f"{idx2dev[k]}/temp", payload=-1, qos=1)
        client.loop(60, 20)
    client.disconnect()