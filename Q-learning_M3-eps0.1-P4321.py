import numpy as np
import random
import pandas as pd

# calculate the next state according to the current state and action
def nextState(state,action):
    (i,j) = state
    if action=='down':
        if i==row-1:
            return state
        next = (i+1,j)
    elif action=='left':
        if j==0:
            return state
        next = (i,j-1)
    elif action=='up':
        if i==0:
            return state
        next = (i-1,j)
    elif action=='right':
        if j == col-1:
            return state
        next = (i,j+1)
    if next in wall:
        next = state
    return next

# define the immediate reward
def immediateReward(state,action,lose):
    if nextState(state,action)== goal:
        return 100
    elif nextState(state,action)== lose:
        return -100
    else:
        return 0

# choose max_Q action
def maxAction(state,Q):
    Qs=[(action,Q[(state,action)]) for action in actions]
    action_max = max(Qs, key=lambda x:x[1])
    index = [j for j,x in enumerate(Qs) if x[1] == action_max[1]]
    if len(index) == 1:
        return action_max[0]
    else:
        return Qs[int(random.choice(index))][0]

def explore():
    return random.choice(actions)

# choose predator area with the defined probability range
def predator(random_seed):
    if random_seed <= prob_predator[0]:
        return random.choice(predator1)
    elif prob_predator[0]< random_seed and random_seed <= prob_predator[1]:
        return random.choice(predator2)
    elif prob_predator[1] < random_seed and random_seed <= prob_predator[2]:
        return random.choice(predator3)
    else:
        preda = []
        return preda

# Greedy functions
def Greedy(state, eps, Q):
    if random.random() < eps:
        return explore()
    else:
        return maxAction(state,Q)

def run_experiment(iteration_n,row,col,discount):
    eps = 1.0
    Q = {}
    discount = discount
    k = 5
    win_N = 0
    Q1 = {}
    Q2 = {}
    Q3 = {}
    Q4 = {}
    Prob_e = []
    Step_to_go = []

    # initial Q-tables
    for i in range(row):
        for j in range(col):
            for action in actions:
                Q1[(i, j), action] = 0
                Q2[(i, j), action] = 0
                Q3[(i, j), action] = 0
                Q4[(i, j), action] = 0

    for episode in range(iteration_n):
        max_step1 = max_step2 = max_step3 = max_step4= max_step= 0
        ''' 
        # case 2
        if ((episode+1) % k) == 0:
            eps = eps / 1.1
        '''
        eps = 0.1 # Please change the value of epsilon to 0.01/0.1/0.3/0.6/0.8
        a = 1

        state1 = startState
        lose1 = predator(0.3) # predator appears in area 1
        while(state1 != goal and state1 != lose1 and max_step1<=600):
            action = Greedy(state1, eps, Q1)
            reward = immediateReward(state1,action,lose1)
            newState1 = nextState(state1,action)
            if (newState1 != state1) and (state1 not in wall):
                # calculate the Q table in the situation where a predator appears in area 1
                Q1[(state1, action)] = (1-a)*Q1[(state1,action)] + a * (reward + discount*Q1[(newState1, maxAction(newState1,Q1))])
            state1 = newState1
            max_step1 = max_step1 + 1

        state2 = startState
        lose2 = predator(0.5) # predator appears in area 2
        while (state2 != goal and state2 != lose2 and max_step2<=600):
            action = Greedy(state2, eps, Q2)
            reward = immediateReward(state2, action, lose2)
            newState2 = nextState(state2, action)
            if (newState2 != state2) and (state2 not in wall):
                # calculate the Q table in the situation where a predator appears in area 2
                Q2[(state2, action)] = (1 - a) * Q2[(state2, action)] + a * (
                            reward + discount * Q2[(newState2, maxAction(newState2, Q2))]) 
            state2 = newState2
            max_step2 = max_step2 + 1

        state3 = startState
        lose3 = predator(0.8) # predator appears in area 3
        while (state3 != goal and state3 != lose3 and max_step3<=600):
            action = Greedy(state3, eps, Q3)
            reward = immediateReward(state3, action, lose3)
            newState3 = nextState(state3, action)
            if (newState3 != state3) and (state3 not in wall):
                # calculate the Q table in the situation where a predator appears in area 3
                Q3[(state3, action)] = (1 - a) * Q3[(state3, action)] + a * (
                        reward + discount * Q3[(newState3, maxAction(newState3, Q3))])
            state3 = newState3
            max_step3 = max_step3 + 1

        state4 = startState
        lose4 = predator(0.95) # predator no appears
        while (state4 != goal and state4 != lose4 and max_step4<=600):
            action = Greedy(state4, eps, Q4)
            reward = immediateReward(state4, action, lose4)
            newState4 = nextState(state4, action)
            if (newState4 != state4) and (state4 not in wall):
                # calculate the Q table in the situation where a predator no appears
                Q4[(state4, action)] = (1 - a) * Q4[(state4, action)] + a * (
                        reward + discount * Q4[(newState4, maxAction(newState4, Q4))])
            state4 = newState4
            max_step4 = max_step4 + 1

        for i in range(row):
            for j in range(col):
                for action in actions:
                    update = prob_predator[0]*Q1[(i,j),action]+(prob_predator[1]-prob_predator[0])*Q2[(i,j),action]+\
                             (prob_predator[2]-prob_predator[1])*Q3[(i,j),action]+(prob_predator[3]-prob_predator[2])*Q4[(i,j),action]
                    Q[(i, j), action] = update # update the Q-table according to Algorithm 1
                    Q1[(i, j), action] = update # update each sub Q-table
                    Q2[(i, j), action] = update
                    Q3[(i, j), action] = update
                    Q4[(i, j), action] = update

        state = startState
        random_seed = random.random()
        lose = predator(random_seed)
        while (state != goal and state != lose and max_step<=600):
            action = Greedy(state, eps, Q)
            newState = nextState(state, action)
            if newState == goal:
                win_N = win_N + 1 # calculate the win game numbers
            state = newState
            max_step = max_step + 1
            if newState == lose:
                max_step = 600
        Step_to_go.append(max_step) # record the step number to go of each experiment

        if (episode == 0):
            Prob_e.append(0)
        if ((episode + 1) % 10 == 0):
            prob = win_N / (episode + 1) # calculate win probability
            Prob_e.append(prob)

    for i in range(row):
        for j in range(col):
            Q_max_ij = max(Q[(i, j), action] for action in actions)
            V[i, j] = Q_max_ij # calculate V table

    return Prob_e,Step_to_go,V # return the win probability, step-to-go, and V table

if __name__ == '__main__':
    row,col = 6,9 # the row and col number of the grid model
    iteration_n = 5000  # iteration number
    run_iteration = 50  # experiment number
    startState = (2, 0)  # the start point
    goal = (0, col - 1)  # goal position
    actions = ['up','down','left','right'] # define the actions
    discount = 0.9 # discount rate
    wall = [(1, 2), (2, 2), (3, 2), (4, 5)]  # define walls' positions
    # The probability of predator appearing in areas 1,2,3 and not appear
    prob_predator = [0.4, 0.7, 0.9, 1]  
    predator1 = [(0, 6), (0, 7)] # area 1
    predator2 = [(1, 6), (1, 7)] # area 2
    predator3 = [(1, 8), (2, 8)] # area 3

    V = np.zeros((row,col),np.float64)
    Prob = []
    Steps = []
    for run in range(run_iteration):
        win_Prob, Step, V_table = run_experiment(iteration_n, row, col, discount)
        Prob.append(win_Prob)
        Steps.append(Step)
        print("the probability of win the game:", run, "the experiments is", win_Prob)
    print("V table of", run, "th run is",V_table)

    average_Prob = (np.array(Prob)).mean(axis=0).round(3) # calculate average win probablity
    average_Steps = (np.array(Steps)).mean(axis=0).round(0) # calculate average step-to-go
    print("average prob is:", average_Prob)
    dict1 = {'probability': average_Prob}
    df1 = pd.DataFrame(dict1)
    df1.to_csv('Q_learning_M3-P4321-eps0.1-50runs5000episode.csv') #record the win probability into a csv file

    dict2 = {'Step': average_Steps}
    df2 = pd.DataFrame(dict2)
    df2.to_csv('Step_M3-P4321-eps0.1.csv') #record the step-to-go into a csv file




