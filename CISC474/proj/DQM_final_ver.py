import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense
import gym
import numpy as np
from pyglet.text import Label
import random
from datetime import datetime

#please check the version of tensorflow is tf 1.14
print("tensorflow_version: " + tf.__version__ + " , please check the version of tensorflow is tf 1.14")
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

class Text:
    def __init__(self, text, x, y, font_size=12, anchor_x="center", anchor_y="center", color=(0, 0, 0, 255)):
        self.text = text
        self.label = Label(text, font_size=font_size, x=x, y=y, anchor_x=anchor_x, anchor_y=anchor_y, color=color, bold=True)

    def render(self):
        self.label.draw()


class MountainCar:
    def __init__(self):
        self.done = False
        self.env = gym.make("MountainCar-v0")
        self.current_state = self.env.reset() # [position, velocity]
        self.action_space_size = self.env.action_space.n
        self.observation_space_high = self.env.observation_space.high
        self.observation_space_low = self.env.observation_space.low
        self.goal_position = self.env.goal_position

    def step(self, action):
        self.current_state, reward, self.done, _ = self.env.step(action)
        return self.current_state, reward, self.done

    def reset(self):
        self.done = False
        self.current_state = self.env.reset()

    def close(self):
        self.env.close()

    def render(self, text=None):
        self.env.render()
        if text is not None:
            geom = Text(str(text), 5, 400, font_size=20, anchor_x="left", anchor_y="top")
            self.env.viewer.add_onetime(geom)


class replayMemory():
    def __init__(self,capacity):
        self.memory = []
        self.temp = []
        self.better = []
        self.capacity = capacity
        self.index = 0
        self.better_index = 0
        self.flush_quad_count = 0

    def push(self,transition):
        #if the common memory is not full add a transition
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        #also add the transition for the temp memory for later use
        self.temp.append(transition)

        #if the common memory is full, change one in it by the index
        self.memory[self.index] = transition
        self.index = (self.index + 1) % self.capacity

    #return a random sample of batch_size from the common memory
    def sample(self,batch_size):
        return random.sample(self.memory, batch_size)
    
    #return a random sample of batch_size from the success(better) memory
    def better_sample(self,batch_size):
        return random.sample(self.better, batch_size)

    #sorting index for the sort function
    def by_score(self,trans):
        return trans[5]

    #adding the temp memory to the success memory
    def add_better(self,score=0):
        index = 0
        
        self.better.sort(key=self.by_score) #sort the success memory by the score(total step used to reach the goal) from low to high(good to bad)
        
        for transition in self.temp:
            if len(self.better) < self.capacity: #if the common memory is not full add the transition
                self.flush_quad_count = 0
                self.better.append(None)
            self.better[self.better_index] = transition + [score]
            self.better_index = (self.better_index + 1) % self.capacity
##            else: #if the common memory is full and the transition is better then the worst one, replace the worse one with the new transition
##                if self.better[(-1 - index)][5] >= score:
##                    self.better[(-1 - index)] = transition + [score]
##                    index += 1
##
##                #after the success memory is full and 100 attempt of update the success memory(success or failed), flush 1/4 of the success memory to let new memory in to make the memory remain diversity
##                self.flush_quad_count += 1
##                if self.flush_quad_count == 100:
##                    self.flush_quad()
##                    self.flush_quad_count = 0
##                    

                
        self.better.sort(key=self.by_score)
                    
                
    def flush_quad(self):
        #ramdomize the success memory
        random.shuffle(self.better)
        
        #delete the last 1/4 of the success memory
        del self.better[int(self.capacity*3/4):]
        
        #reset the index for the success memory
        self.better_index = len(self.better)

    #flush the temp memory
    def flush_temp(self):
        self.temp = []

    def __len__(self):
        return len(self.memory)

    def __betterLen__(self):
        return len(self.better)

class DQN():
    def __init__(self,alpha=3e-4, gamma=0.9, epsilon=1, memory_capacity=16000,load_model=None):
        #record the loss and reward for grahing use
        self.loss_episode = []
        self.loss = []
        self.reward = []
        
        
        #hyper-parameters for DQN
        self.epsilon = epsilon
        self.epsilon_decay = 0.005
        self.epsilon_min = 0.01
        self.alpha = alpha
        self.gamma = gamma
        
        #set the batch_size at 64
        self.batch_size = 64

        #environment and the replay memory
        self.env = MountainCar()
        self.replayMemory = replayMemory(memory_capacity)
        self.state_size = len(self.env.env.state)

        #create main model and target model
        self.model = self.init_model()
        self.target_model = self.init_model()
        
        #load the model 
        if load_model != None:
            self.model.load_weights(load_model)

            
        #Sync the target model and main model
        self.update_target_model()
        
        

    #update the target model to have the same weights with the main model
    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())
        
    #function to initialize the model
    def init_model(self):
        # the model structure with two hidden layer for this environment, input is shape(2,) output is in 3 dimension
        model = Sequential([
            Input(shape=self.env.current_state.shape),
            Dense(24, activation="relu"),
            Dense(24, activation="relu"),
            Dense(self.env.action_space_size, activation="linear")
        ])
        model.compile(loss='mse', optimizer=Adam(lr=self.alpha))
        return model

    #return the action with e-greedy algrothim
    def get_action(self,state):
        #make the epsilon not exeecd the lower bound
        self.epsilon = max(self.epsilon_min, self.epsilon)
        
        if random.random() <= self.epsilon:
            return random.randrange(self.env.action_space_size) # with epsilon prob return a random action
        else:
            q_value = self.model.predict(state) # else return the action based on the DQN output
            return np.argmax(q_value[0])
            

    def train_from_memory(self,batch_mult=10):
        #do not train before memory is filled to some threshold which is set to 10*batch_size
        if self.replayMemory.__len__() < self.batch_size * batch_mult:
            return
        
        #receive a mini batch sample from the memory
        if (self.replayMemory.__betterLen__() > self.batch_size * batch_mult): #if there is enough success experience, select 0.8 of batch_size from the success experience, 0.2 from common experience
            mini_batch = self.replayMemory.better_sample(int(self.batch_size*0.8))
            mini_batch = mini_batch+self.replayMemory.sample(int(self.batch_size - int(self.batch_size*0.8)))
        else:                                                               #otherwise select a batch_size example from the common experience
            mini_batch = self.replayMemory.sample(self.batch_size) 

        #init the data set for the mini batch tarining
        batch_input = np.zeros((self.batch_size,self.state_size))
        batch_target_input = np.zeros((self.batch_size,self.state_size))
        batch_actions,batch_rewards,batch_done = [],[],[]

        #fill up the mini batch
        for i in range(self.batch_size):
            batch_input[i] = mini_batch[i][0]
            batch_actions.append(mini_batch[i][1])
            batch_rewards.append(mini_batch[i][2])
            batch_target_input[i] = mini_batch[i][3]
            batch_done.append(mini_batch[i][4])

        

        #Get the Q value of each state and next state
        pred_val = self.model.predict(batch_input)
        target_pred_val = self.target_model.predict(batch_target_input)
        

        #this is the Q learning update equaltion   
        for i in range(self.batch_size):
            if batch_done[i]:
                pred_val[i][batch_actions[i]] = batch_rewards[i] #y^j is r^j for terminal state
            else:
                pred_val[i][batch_actions[i]] = batch_rewards[i] + self.gamma*(np.amax(target_pred_val[i])) #y^j is r^j + γQmax（s^j+1）for terminal state

        #compute the loss and train the model(apply the gradient descent)
        loss = self.model.train_on_batch(batch_input,pred_val)
        self.loss_episode.append(loss) #record the loss 
            
    
    def train(self,episodes=10000,save_data = False,render=False):
        
        #visualize the process
        if render:
            self.env.render()
        
        score = 0
        succeed_count = 0
        
        for episode in range(episodes):
            
            #initialize the environment
            self.env.reset()
            
            
            step = 0
            state = self.env.current_state
            state = np.reshape(state, [1,self.state_size])
            

            while not self.env.done:
                step += 1
                #get the action based on the state 
                action = self.get_action(state)

                #get feed back from the environment based on the action chosen
                next_state, reward, done = self.env.step(action)
                next_state = np.reshape(next_state, [1,self.state_size])

                #push the transition in to the normal memory
                self.replayMemory.push([state,action,reward,next_state,done])

                #train the model using the mini batch from the replayMemory
                self.train_from_memory()

                #score is avg cumulative reward for 100 episode
                score += reward
                first_action = action
                state = next_state

            
            #save the data if save_data = True
            if save_data and len(self.loss_episode)>0:
                self.loss.append((sum(self.loss_episode)/len(self.loss_episode)))
                self.reward.append(-step)

            #flush the loss memory for the episode
            self.loss_episode = []

            
            #update the target model after every episode   
            self.update_target_model()

            #if episode finished with the goal reached, add the memory to the better replay memory cache
            if done and step < 200:
                succeed_count += 1
                self.replayMemory.add_better(step)
        
            #flush the temp memory storge for the episode
            self.replayMemory.flush_temp()

            #training information per 100 episode
            if (episode+1) % 100 == 0:
                try:
                    print("average reward: " + str(score/100) + " with episode =" + str(episode+1) + " ,finish rate =" + str(succeed_count/100) + ", better_len : " + str(self.replayMemory.__betterLen__()) + ", max_better_step : " + str(self.replayMemory.better[-1][5]))
                except:
                    print("average reward: " + str(score/100) + " with episode =" + str(episode+1) + " ,finish rate =" + str(succeed_count/100) + ", better_len : " + str(self.replayMemory.__betterLen__()))
                succeed_count = 0
                score = 0

            #make epsilon decay per episode up to a limit
            self.epsilon -= self.epsilon_decay

            #save model and data(if save_data) per 100 episode
            if (episode+1) % 100 == 0:
                self.save_model("withBetterMemory_0.8_normal_16000size_" + str(episode+1))
                if save_data:
                    np.savetxt("withBetterMemory_0.8_16000size_flush_loss" + str(episode+1),np.asarray(self.loss),delimiter=',')
                    np.savetxt("withBetterMemory_0.8_16000size_flush_reward" + str(episode+1),np.asarray(self.reward),delimiter=',')


                
            
    #function to test the model
    def test_model(self,episodes=500,render=False):
                
        #visualize the process
        if render:
            self.env.render()
            
        score = 0
        succeed_count = 0
        
        for episode in range(episodes):
            
            #initialize the environment
            self.env.reset()
            
            state = self.env.current_state
            state = np.reshape(state, [1,self.state_size])
            

            while not self.env.done:
                #get the action based on the state 
                action = self.get_action(state)

                #get feed back from the environment based on the action chosen
                next_state, reward, done = self.env.step(action)
                next_state = np.reshape(next_state, [1,self.state_size])


                #score is avg cumulative reward for all the testing episode
                score += reward
                first_action = action
                state = next_state

            #testing information per 100 episode
            if (episode+1) % 100 == 0:
                print("average reward: " + str(score/(episode+1)) + " with episode =" + str(episode+1) + " ,finish rate =" + str(succeed_count/(episode+1)))


                
        
    def save_model(self, name):
        current_time = datetime.now()
        self.model.save(f"{name}_{current_time.strftime('%Y_%m_%d_%H_%M_%S')}.h5")




if __name__ ==  "__main__":
    #create the instance
    DQN_agent = DQN(load_model="withOnlyBetterMemory_0.8_16000size_100_2019_11_26_08_39_16.h5")

    #training function
    print("start training")
    DQN_agent.train(save_data=True)

    #use this code for testing
    #please load the model for the agent instance first
    #using DQN_agent(load_model=fname,epsilon=0.01)
    #DQN_agent.test_model()











