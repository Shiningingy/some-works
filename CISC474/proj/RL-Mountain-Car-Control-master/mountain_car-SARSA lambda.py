import gym
import numpy as np

#Initialization
env = gym.make("MountainCar-v0")
env.reset()

#Variables required
LEARNING_RATE = 0.5
DISCOUNT = 0.95
EPISODES = 15000
SHOW_EVERY = 500
Q_TABLE_LEN = 20
DISCRETE_OS_SIZE = [Q_TABLE_LEN] * len(env.observation_space.high)
discrete_os_win_size = (env.observation_space.high - env.observation_space.low) / DISCRETE_OS_SIZE
q_table = np.random.uniform(low=0, high=1,size=(DISCRETE_OS_SIZE + [env.action_space.n]))
epsilon = 1  
START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = EPISODES//2
epsilon_decay_value = epsilon/(END_EPSILON_DECAYING - START_EPSILON_DECAYING)
LAMBDA = 0.95
e_trace = np.zeros((DISCRETE_OS_SIZE + [env.action_space.n]))


#helper functions
def get_discrete_state (state):
    discrete_state = (state - env.observation_space.low) // discrete_os_win_size
    return tuple(discrete_state.astype(int))

def take_epilon_greedy_action(state, epsilon):
    discrete_state = get_discrete_state(state)
    if np.random.random() < epsilon:
        action = np.random.randint(0,env.action_space.n)
    else:
        action = np.argmax(q_table[discrete_state])
    return action

##SARSA lambda

for episode in range(EPISODES):
    state = env.reset()
    action = take_epilon_greedy_action(state, epsilon)
    
    e_trace = np.zeros(DISCRETE_OS_SIZE + [env.action_space.n])
    
    done = False
    ep_reward = 0
    while not done:
        next_state, reward, done, _ = env.step(action)
        ep_reward += reward
        
        next_action = take_epilon_greedy_action(next_state, epsilon)
        if not done:
            
            delta = reward + DISCOUNT * q_table[get_discrete_state(next_state)][next_action] - q_table[get_discrete_state(state)][action]
            e_trace[get_discrete_state(state)][action] += 1            
            q_table += LEARNING_RATE * delta * e_trace            
            e_trace = DISCOUNT * LAMBDA * e_trace
            
        elif next_state[0] >= 0.5:
#            print("I made it on episode: {} Reward: {}".format(episode,reward))
            q_table[get_discrete_state(state)][action] = 0
        state = next_state
        action = next_action
    if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
        epsilon -= epsilon_decay_value

#Visualization
done = False
state = env.reset()
while not done:
    action = np.argmax(q_table[get_discrete_state(state)])
    next_state, _, done, _ = env.step(action)
    state = next_state
    env.render()
    
env.close()
