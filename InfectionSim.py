''' Simple Infection Simulation
-Agent based model
-Checker board style random movement
-Simple infection probability
-Base case with civilian and medic
-Outputs to a csv file
'''

###TO_DO###
# -Infection Probability
# -Arguments from commandline
# -Simplify y coordinate generation
# -Natural recovery time

import random
import csv

__author__ = "Hayley Oliver"
__version__ = '1.1'

class InfectionSim():
    ''' Simulation Class'''
    def __init__(self, end_t, num_healthy, num_infected, num_medic, infection_p):
        self.end_t = end_t
        self.num_healthy = num_healthy
        self.num_infected = num_infected
        self.num_medic = num_medic
        self.infection_p = infection_p
        self.recovered_count = 0
        self.infection_count = 0
        self.agent_list = []
        self.board_size = 10
        self.board = []

    def generate_agents(self):
        '''Generates instances of class Agent with parameters specified.'''
        for i in range(self.num_healthy):
            self.agent_list.append(Agent("Civ", False))
        for i in range(self.num_infected):
            self.agent_list.append(Agent("Civ", True))
        for i in range(self.num_medic):
            self.agent_list.append(Agent("Med", False))

    def x_movement(self, int, x):
        ''' Generates new X coordinate based on a random integer'''
        new_x = x + ((int % 3)-1)
        if new_x < 0: new_x = 0
        if new_x > 9: new_x = 9
        return new_x

    def y_movement(self, int, y):
        ''' Generates new Y coordinate based on random integer'''
        if int <= 2 and int >= 0:
            new_y = y + 1
        elif int <= 5 and int >= 3:
            new_y = y
        elif int <= 8 and int >= 6:
            new_y = y - 1
        if new_y < 0: new_y = 0
        if new_y > 9: new_y = 9
        return new_y

    def tags(self):
        '''
        Generates a two dementional array representing the simulation board.
        Each entry contains a tag representing the position on the board.
        '''
        for i in range(self.board_size):
            self.board.append([])

        for i in range(len(self.board)-1, -1, -1):
            col = ["A","B","C","D","E","F","G","H","I","J"]
            for n in col:
                n = n + str(i)
                self.board[i].append(n)

    def collision_check(self):
        '''
        Checks for collision between agents and preforms approprate event.
        Appends position tags of infected, healthy, and medics to respective list.
        Sets number of healthy and infected agents and checks for infection and recovery.
        '''
        infected_tag = []
        healthy_tag = []
        medic_tag = []
        for agent in self.agent_list:
            if agent.state == True:
                infected_tag.append(agent.tag)
            elif agent.state == False:
                healthy_tag.append(agent.tag)
            if agent.role == "Med":
                medic_tag.append(agent.tag)
        self.num_healthy = len(healthy_tag)
        self.num_infected = len(infected_tag)
        for tag in infected_tag:
            if tag in healthy_tag:
                for agent in self.agent_list:
                    if agent.tag == tag and agent.state == False:
                        if random.random() <= self.infection_p:
                            agent.state = True
                            self.infection_count += 1
                            self.num_healthy -= 1
                            self.num_infected += 1

            if tag in medic_tag:
                for agent in self.agent_list:
                    if agent.tag == tag and agent.state == True:
                        agent.state = False
                        self.recovered_count += 1
                        self.num_healthy += 1
                        self.num_infected -= 1

    def generate_file(self, mode, *args):
        '''Generates data file with inputs'''
        with open('InfectionSim.csv', mode) as file:
            writer = csv.writer(file)
            data = []
            for i in args:
                data.append(i)
            writer.writerow(data)

    def run(self):
        '''
        Main method. Calls method to generate agents and board.
        Adds headers to the data output file.
        At every timestep, generates random movement and checks for collision.
        For every collision, infection occures at infection_p
        '''
        self.generate_agents()
        self.tags()
        self.generate_file("w","Time","NumInfected","NumHealthy","NumMedic","NumRecovered","NumInfections")
        for t in range(0, self.end_t + 1):
            if t == 0:
                for agent in self.agent_list:
                    rx = random.randint(0,9)
                    ry = random.randint(0,9)
                    agent.x = rx
                    agent.y = ry
                    agent.tag = self.board[agent.x][agent.y]
                self.generate_file('a',t,self.num_infected,self.num_healthy,self.num_medic)
                #print "Time: ", t, "# infected: ", self.num_infected, "# healthy: ", self.num_healthy
                t += 1
            else:
                for agent in self.agent_list:
                    rand = random.randint(0,8)
                    agent.x = self.x_movement(rand, agent.x)
                    agent.y = self.y_movement(rand, agent.y)
                    agent.tag = self.board[agent.x][agent.y]
                self.collision_check()
                self.generate_file('a',t,self.num_infected,self.num_healthy,self.num_medic,self.recovered_count,self.infection_count)
                #print "Time: ", t, "# infected: ", self.num_infected, "# healthy: ", self.num_healthy, "# recovered: ", self.recovered_count, "# infections: ", self.infection_count
                t += 1


class Agent():
    '''Creates and instance of an agent with the given parameters'''
    def __init__(self, role, state):
        '''
        Each agent has attribute role, x, y, tag, and state.
        Role = medic or civilian
        x, y = coordinates of the agent on the board
        tag = position tag that identifies the agents position for collision check
        '''
        self.role = role
        self.x = 0
        self.y = 0
        self.tag = ""
        self.state = state

InfectionSim(100, 20, 2, 2, 0.5).run()
