import db
import time
import random
from db import DBPATH

dbcon = db.create_connection(DBPATH)
MAX_VENT = 6
idx2dev = {}

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
    reward = -0.5 # cost per step

    hot_list = []
    cold_list = []
    if action == 0:  # from hottest to coldest
        temp = state[:-1]
        hot = max(temp)
        hot_index = temp.index(hot)
        cold = min(temp)
        cold_index = temp.index(cold)
        new_cold = cold + state[-1] / MAX_VENT
        new_hot = hot - state[-1] / MAX_VENT
        hot_list.append((hot_index, new_hot))
        cold_list.append((cold_index, new_cold))
    elif action == 1:  # from hottest to all
        temp = state[:-1]
        hot = max(temp)
        hot_index = temp.index(hot)
        new_hot = hot - state[-1] / MAX_VENT
        hot_list.append((hot_index, new_hot))
        for index, v in enumerate(temp):
            if index != hot_index:
                cold_list.append((index, v + (state[-1] / MAX_VENT)/(len(temp) - 1)))
    elif action == 2:  # from hottest to temp < avg
        temp = state[:-1]
        hot = max(temp)
        hot_index = temp.index(hot)
        new_hot = hot - state[-1] / MAX_VENT
        hot_list.append((hot_index, new_hot))
        avg = sum(temp) / len(temp)
        l = sum(1 for t in temp if t < avg)
        for index, v in enumerate(temp):
            if v < avg:
                cold_list.append((index, v + (state[-1] / MAX_VENT)/l))
    # print(hot_list)
    # print(cold_list)
    # send to devices changes in temp
    for hot_index, new_hot in hot_list:
        db.add_vent(dbcon, idx2dev[hot_index], new_hot)
    for cold_index, new_cold in cold_list:
        db.add_vent(dbcon, idx2dev[cold_index], new_cold)

    time.sleep(2)

    # read new temp
    next_state = get_state(state[-1])

    # generate reward
    avg = sum(next_state[:-1]) / len(next_state[:-1])
    for t in next_state[:-1]:
        reward -= abs(t - avg)/2
    reward -= next_state[-1] * 0.07 * 0.5

    # if equals -> done
    avg = sum(next_state[:-1]) / len(next_state[:-1])
    for t in next_state[:-1]:
        if abs(avg - t) > 0.5:
            return next_state, reward, False
    return next_state, reward, True

def vent_off():
    db.remove_vent(dbcon)