import Connect4
import Agent
import json
import numpy as np


if __name__ == '__main__':
    
    players = [Agent.DeepQLearningAgent(42, 7), Agent.DeepQLearningAgent(42, 7)]
    #players = [Agent.DeepQLearningAgent(42, 7), 'Human']

    for i in range(100000):
        game = Connect4.GameBoard()
        
        step = 0
        finish = False
        temp_state = np.array([])
        oppt_state = np.array([])
        temp_action = 0
        while finish == False:

            t = step % 2
            
            if type(players[t]) == Agent.DeepQLearningAgent:
                players[t].load_data()
                
                curr_state = game.getState(step)
                temp_state = game.getState(step)
                temp2_state = game.getState(step - 1)
                #print(temp2_state)
                curr_action = players[t].get_action(temp2_state)
                while game.is_valid_col(curr_action) == False:
                    curr_action = players[t].get_random_action(temp2_state)
                finish = game.move(curr_action, step)
                
                if game.is_draw():
                    finish = True
                
                reward = 1
                if finish:
                    players[t].remember(oppt_state, temp_action, -9999, temp2_state, finish)
                    players[t].replay(players[t].batch_size)
                    reward = 100
                
                oppt_state = temp_state
                temp_action = curr_action
                
                players[t].remember(curr_state, curr_action, reward, game.getState(step), finish)
                players[t].replay(players[t].batch_size)
                players[t].save_data()
                
                if i % 10 == 0:
                    print('step:', step)
                    print(game)
            else:
#                 curr_state = game.getState(step)
#                 temp_state = game.getState(step)
#                 temp2_state = game.getState(step - 1)
                print(game)
                
                finish, curr_action = game.input_col(t + 1)
#                 
#                 if game.is_draw():
#                     finish = True
#                     
#                 reward = 0
#                 if finish:
#                     players[0].remember(oppt_state, temp_action, -100, temp2_state, finish)
#                     players[0].replay(players[0].batch_size)
#                     reward = 1
#                 
#                 oppt_state = temp_state
#                 temp_action = curr_action
#                     
#                 players[0].remember(curr_state, curr_action, reward, game.getState(step), finish)
#                 players[0].replay(players[0].batch_size)
#                 players[0].save_data()
                
            step = step + 1
        
        print('Round:', i + 1, step - 1)
        
    print('END')