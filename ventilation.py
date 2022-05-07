import torch
import db
import sys
import env
import agent
import numpy as np
import time
from db import DBPATH

if len(sys.argv) < 4:
    print(f"Usage: {sys.argv[0]} <ventilation_force> <state_size> <action_size>")
    exit()
ventilation = int(sys.argv[1])
state_size = int(sys.argv[2])
action_size = int(sys.argv[3])
dbcon = db.create_connection(DBPATH)
model = agent.Model(state_size, action_size)
model.load_state_dict(torch.load("models/20_model_state_dict"))
model.eval()
current_state = env.get_state(ventilation)
done = False
print("Ventilation start")
while not done:
    with torch.no_grad():
        action = np.argmax(model(torch.from_numpy(np.vstack([current_state])).float()))
    state_, reward, done = env.step(current_state, action)
    current_state = state_.copy()
print("Ventilation end")
time.sleep(10)
env.vent_off()