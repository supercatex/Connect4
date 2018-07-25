import random, json, os
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

class QLearningAgent:

    #Q-learning
    learning_rate = 0   #alpha
    discount_factor = 1 #gamma
    greedy = 0          #greedy
    Q = {}              #initial conditions

    #data files
    filename = './data.json'
    training = 0


    #constructor
    def __init__(self,
                 learning_rate = 0.1,
                 discount_factor = 0.9,
                 greedy = 0.9):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.greedy = greedy


    #Load data.
    #params: none
    #return: void
    def load_data(self):
        if not os.path.exists(self.filename):
            f = open(self.filename, 'w')
            f.write('')
            f.close()
            
        f = open(self.filename, 'r')
        data = f.readlines()
        f.close()
        if len(data) > 0:
            temp = json.loads(data[0])
            self.training = int(temp['0'])
            self.Q = temp['1']


    #Save data.
    #params: none
    #return: void
    def save_data(self):
        data = json.dumps({'0': self.training, '1': self.Q})
        f = open(self.filename, 'w')
        f.write(data)
        f.close()


    #Q-learning study method.
    #params:
    #   observations: dict
    #   action: string
    #   next_observations: dict
    #   reward: number
    #return: next observations
    def study(self, observations, action, next_observations, reward):
        state = self.get_key(observations)

        next_state = self.get_key(next_observations)
        next_action = self.get_optimal_action(next_observations)
        
        #Q[n]
        old_value = self.Q[state][action]
        #Q[n+1]
        future_value = self.Q[next_state][next_action]

        #Q[n] <- Q[n] + a * (R[n] + y * Q[n+1] - Q[n])
        self.Q[state][action] = old_value + self.learning_rate * (reward + self.discount_factor * future_value - old_value) 

        #self.training = self.training + 1
        return next_observations


    #print Q.
    #params: none
    #return: void
    def print_Q(self):
        for state, actions in self.Q.items():
            print(str(state) + ': ' + str(actions))

    def get_Q_zero_count(self):
        count = 0
        for state, actions in self.Q.items():
            for action, value in actions.items():
                if value == 0:
                    count += 1
        return count

    def get_Q_max_value(self):
        v = 0
        for state, actions in self.Q.items():
            for action, value in actions.items():
                if value > v:
                    v = value
        return v

    def get_Q_min_value(self):
        v = 0
        for state, actions in self.Q.items():
            for action, value in actions.items():
                if value < v:
                    v = value
        return v
                

    #get a randomize action by observations.
    #params:
    #   observations : dict
    #return: string
    def get_random_action(self, observations):
        state = self.get_key(observations)
        actions = list(self.Q[state].keys())
        if len(actions) == 0: return ''
        
        rand = random.randint(0, len(actions) - 1)
        return actions[rand]


    #get a optimal action by observations.
    #params:
    #   observations : dict
    #return: string
    def get_optimal_action(self, observations):
        state = self.get_key(observations)
        actions = list(self.Q[state].keys())
        if len(actions) == 0: return ''

        #random action order
        for i in range(0, len(actions)):
            rand = random.randint(0, len(actions) - 1)
            temp = actions[i]
            actions[i] = actions[rand]
            actions[rand] = temp

        #get the max one
        action = actions[0]
        max_value = self.Q[state][action]
        for i in range(1, len(actions)):
            if self.Q[state][actions[i]] > max_value:
                action = actions[i]
                max_value = self.Q[state][actions[i]]
        return action


    #get a action by observations.
    #params:
    #   observations : dict
    #return: string
    def get_action(self, observations):
        if random.random() < self.greedy:
            return self.get_optimal_action(observations)
        else:
            return self.get_random_action(observations)

    
    #add a new state
    #params:
    #   observations : dict
    #   actions : array
    #return: void
    def add_state(self, observations, actions):
        state = self.get_key(observations)
        if state in self.Q:
            return

#         print ( state )
#         print ( observations )
        
#         existed_keys = {}
#         existed_errs = 0
#         for key1, val1 in self.Q.items():
#             obj1 = json.loads(key1)
#             temp = {}
#             errs = 0
#             for key2, val2 in observations.items():
#                 if key2 in obj1:
#                     temp.update({key2: obj1[key2]})
#                     errs += np.mean((np.array(obj1[key2]) - np.array(val2)) ** 2)
#             if len(temp) > len(existed_keys):
#                 existed_keys = temp
#                 existed_errs = errs
#             elif len(temp) == len(existed_keys):
#                 if existed_errs > errs:
#                     existed_keys = temp
#                     existed_errs = errs
#         
#         if len(existed_keys) > 0:
#             temp = self.get_key(existed_keys)
#             if temp in self.Q:
#                 self.Q[state] = {}
#                 for i in range(0, len(actions)):
#                     self.Q[state][actions[i]] = self.Q[temp][actions[i]]
#                 return
        
        #renew Q
        self.Q[state] = {}
        #actions = self.get_actions(observations)
        for i in range(0, len(actions)):
            self.Q[state][actions[i]] = 0


    #named state by observations
    #params:
    #   observations : dict
    #return: string
    def get_key(self, observations):
        temp = '{'
        keys = sorted(list(observations.keys()))
        for i in range(0, len(keys) - 1):
            temp += '\'' + str(keys[i]) + '\': ' + str(observations[keys[i]]) + ', '
        if len(keys) > 0:
            temp += '\'' + str(keys[len(keys) - 1]) + '\': ' + str(observations[keys[len(keys) - 1]]) + ''
        temp += '}'
        return temp


class DeepQLearningAgent:
    
    def __init__(self, 
                 state_size, 
                 action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1     # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.1
        self.batch_size = 32
        self.filename = './data.h5'
        self.model = self._build_model()


    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))


    def get_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def get_random_action(self, state):
        return np.random.randint(0, self.action_size)

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


    def load_data(self):
        if os.path.exists(self.filename):
            self.model.load_weights(self.filename, True)


    def save_data(self):
        self.model.save_weights(self.filename, True)

