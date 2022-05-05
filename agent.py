from collections import deque, namedtuple
import torch
import torch.nn as nn
import torch.nn.functional as F
import random
import numpy as np
import env

Transition = namedtuple('Transition', ('state', 'action', 'reward', 'state_', 'done'))
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class ReplayMemory():
    def __init__(self, capacity):
        self.memory = deque([],maxlen=capacity)
        self.experience = namedtuple('experience', ('state', 'action', 'reward', 'state_', 'done'))

    def push(self, state, action, reward, state_, done):
        e = self.experience(state.copy(), action, reward, state_.copy(), done)
        self.memory.append(e)

    def sample(self, batch_size):
        experiences = random.sample(self.memory, batch_size)

        states = torch.from_numpy(np.vstack([e.state for e in experiences if e is not None])).float().to(device)
        actions = torch.from_numpy(np.vstack([e.action for e in experiences if e is not None])).long().to(device)
        rewards = torch.from_numpy(np.vstack([e.reward for e in experiences if e is not None])).float().to(device)
        next_states = torch.from_numpy(np.vstack([e.next_state for e in experiences if e is not None])).float().to(device)
        dones = torch.from_numpy(np.vstack([e.done for e in experiences if e is not None]).astype(np.uint8)).float().to(device)
  
        return (states, actions, rewards, next_states, dones)

class Model(nn.Module):
    def __init__(self, state_size, action_size, layer1=64, layer2=64):
        self.l1 = nn.Linear(state_size, layer1)
        self.l2 = nn.Linear(layer1, layer2)
        self.l3 = nn.Linear(layer2, action_size)

    def foward(self, x):
        x = x.to(device)
        x = F.relu(self.l1(x))
        x = F.relu(self.l2(x))
        return self.l3(x)

BATCH_SIZE = 64
MEMORY_SIZE = 10000
GAMMA = 0.99
TAU = 1e-3
LR = 5e-4
EPS = 1.0
EPS_MIN = 0.02
EPS_DECAY = 0.995
EPISODES = 10

class Agent():
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.batch_size = BATCH_SIZE
        self.gamma = GAMMA
        self.tau = TAU
        self.lr = LR
        self.eps = EPS
        self.eps_decay = EPS_DECAY
        self.eps_min = EPS_MIN
        self.episodes =EPISODES

        self.net = Model(state_size, action_size).to(device)
        self.target_net = Model(state_size, action_size).to(device)
        self.memory = ReplayMemory(MEMORY_SIZE)
        self.optimizer = torch.optim.Adam(self.net.parameters(), lr=LR)

    def fit_model(self):
        states, actions, rewards, states_, dones = self.memory.sample(self.bath_size)

        Q_target_next = self.target_net(states_).detach().max(1)[0].unsqueeze(1)
        Q_targets = rewards + self.gamma * Q_target_next * (1 - dones)
        Q_exp = self.net(states).gather(1, actions)

        loss = F.mse_loss(Q_exp, Q_targets)
        loss.backward()
        self.optimizer.step()

    def soft_target_update(self):
        for target_param, net_param in zip(self.target_net.parameters(), self.net.parameters()):
            self.target_net.data.copy_(self.tau*net_param.data + (1.0-self.tau)*target_param.data)

    def train(self):
        reward_list = []
        for e in range(self.episodes):
            self.optimizer.zero_grad()

            state = env.get_state()
            done = False
            reward_e = 0
            
            # collect episode data
            while not done:
                if random.random() <= self.eps:
                    action = random.randrange(0, self.action_size)
                else:
                    self.net.eval()
                    with torch.no_grad():
                        action = np.argmax(self.net(state))
                    self.net.train()

                state_, reward, done = env.step(state, action)

                self.memory.push(state.copy(), action, reward, state_.copy(), done)

                reward_e += reward
                state = state_.copy()

            self.eps = max(self.eps_min, self.eps*self.eps_decay)

            self.fit_model()
            self.soft_target_update()

            reward_list.append(reward_e)
            print(f"episode: {e}, reward: {reward_e}")