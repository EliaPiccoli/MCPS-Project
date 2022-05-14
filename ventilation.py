import torch
import db
import sys
import env
import agent
import numpy as np
import time
from db import DBPATH

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <ventilation_force>")
    exit()
ventilation = int(sys.argv[1])
state_size = 6
action_size = 3
dbcon = db.create_connection(DBPATH)
model = agent.Model(state_size, action_size)
model.load_state_dict(torch.load("models/ventilation_model/120_model_state_dict"))
model.eval()
current_state = env.get_state(ventilation)
done = False
print("Ventilation start")
steps=0
while not done:
    steps+=1
    with torch.no_grad():
        action = np.argmax(model(torch.from_numpy(np.vstack([current_state])).float()))
    state_, reward, done = env.step(current_state, action)
    current_state = state_.copy()
print(f"Ventilation end in {steps} steps")
time.sleep(10)
env.vent_off()