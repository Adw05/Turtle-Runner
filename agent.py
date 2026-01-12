import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import random
import numpy as np
from collections import deque
import os


class DQN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class Agent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=100000)  # Increased memory size slightly
        self.gamma = 0.99  # Discount rate
        self.epsilon = 1.0  # Exploration rate (managed by main.py)
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.lr = 0.001

        # --- GPU DETECTION ---
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Agent using device: {self.device}")

        # Initialize Model and move to GPU
        self.model = DQN(state_size, 256, action_size).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)

    def choose_action(self, state):
        # 1. Random Move (Exploration)
        if random.random() < self.epsilon:
            return random.randint(0, self.action_size - 1)

        # 2. Predicted Move (Exploitation)
        state_tensor = torch.FloatTensor(state).to(self.device)
        self.model.eval()  # Set to evaluation mode
        with torch.no_grad():
            q_values = self.model(state_tensor)
        self.model.train()  # Set back to training mode

        return torch.argmax(q_values).item()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def learn(self, batch_size=64):
        if len(self.memory) < batch_size:
            return

        batch = random.sample(self.memory, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        # Convert to Tensors and move to GPU
        # NOTE: np.array is used first to prevent the "Slow" UserWarning
        states = torch.FloatTensor(np.array(states)).to(self.device)
        actions = torch.LongTensor(np.array(actions)).unsqueeze(1).to(self.device)
        rewards = torch.FloatTensor(np.array(rewards)).unsqueeze(1).to(self.device)
        next_states = torch.FloatTensor(np.array(next_states)).to(self.device)
        dones = torch.FloatTensor(np.array(dones)).unsqueeze(1).to(self.device)

        # 1. Predicted Q values (Current State)
        q_values = self.model(states).gather(1, actions)

        # 2. Target Q values (Next State)
        with torch.no_grad():
            q_next = self.model(next_states).max(1)[0].unsqueeze(1)
            target = rewards + (self.gamma * q_next * (1 - dones))

        # 3. Calculate Loss and Optimize
        loss = F.mse_loss(q_values, target)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.model.state_dict(), file_name)
    def load(self, file_name='model.pth'):
        model_folder_path = './model'
        file_path = os.path.join(model_folder_path, file_name)
        if os.path.exists(file_path):
            self.model.load_state_dict(torch.load(file_path))
            self.model.eval()
            print(f"Model loaded successfully from {file_path}")
        else:
            print(f"Error: No model found at {file_path}")
