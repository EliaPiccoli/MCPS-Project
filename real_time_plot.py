import db
import matplotlib.pyplot as plt
import keras
import numpy as np
import sys
from datetime import datetime
from db import DBPATH

PAST=40
FUTURE=20
INPUT_SIZE=10

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <device_name> <?past_data> <?future_data>")
    exit()
elif len(sys.argv) == 4:
    PAST = int(sys.argv[2])
    FUTURE = int(sys.argv[3])
elif len(sys.argv) == 3:
    PAST = int(sys.argv[2])
    FUTURE = 0
else:
    PAST=40
    FUTURE=20
    
device = sys.argv[1]

dbcon = db.create_connection(DBPATH)
model = keras.models.load_model(f"models/{device}_model")
while True:
    plt.clf()
    ans = db.get_device_temp_ord(dbcon, device, PAST)
    temp = [t[0] for t in ans[::-1]]
    exp_temp = [temp[-1]]
    inp = np.array([temp[-INPUT_SIZE:]])
    for i in range(FUTURE):
        next_temp = model.predict(np.reshape(inp, (inp.shape[0], 1, inp.shape[1])))
        exp_temp.append(next_temp[0][0])
        a = []
        for i in range(1, INPUT_SIZE):
            a.append(inp[0][i])
        a.append(next_temp[0][0])
        inp = np.array([a])
    plt.title(f"Temperature {device} - Time: {datetime.fromisoformat(ans[0][1]).hour:02d}:{datetime.fromisoformat(ans[0][1]).minute:02d}")
    plt.plot(range(len(temp)), temp, "b", label='Past temperatures')
    if FUTURE > 0:
        plt.plot(range(len(temp)-1, len(temp)+len(exp_temp)-1), exp_temp, "r", label='Future temperatures')
    plt.ylabel("Temperature [°C]")
    plt.xlabel("Time")
    plt.legend()
    plt.show(block=False)
    plt.pause(1)