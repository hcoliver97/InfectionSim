''' Simple Infection Simulation For Processing
-Agent based model
-Checker board style random movement
-Simple infection probability from distribution
-Natural recovery from triangle distribution
-Base case with civilian and medic
-Enter parameters at bottom of InfectionSim.py
-Run in processing to generate visual of random movement
'''

###TO_DO###
# Important:
# -Quarentine
# -Code batch runner file
# -Organize code
#
# -Arguments from commandline
# -Simplify y coordinate generation
# -Come up with position tag system that can handle bigger boards
# -Initial number infected by probability?

import random
import csv
from Rv import Triangle
import time

__author__ = "Hayley Oliver"
__version__ = '1.6.1'

class InfectionSim(Triangle):
    ''' Simulation Class'''
    def __init__(self, end_t, num_medic, infection_p, recovery_t, *args):
        Triangle.__init__(self)
        # User input variables
        self.end_t = end_t
        self.num_medic = num_medic
        self.infection_p = Triangle().generate(infection_p[0],infection_p[1],infection_p[2])
        self.recovery_t = Triangle().generate(recovery_t[0],recovery_t[1],recovery_t[2])
        self.squad = args
        # Initialization variables
        self.num_healthy = 0
        self.num_infected = 0
        self.infected_tag = []
        self.healthy_tag = []
        self.medic_tag = []
        self.recovered_count = 0
        self.infection_count = 0
        self.infection_cord = []
        self.recovery_cord = []
        self.agent_list = []
        self.board_size = 20
        self.board = []
        self.t = 0

    def generate_agents(self):
        '''Generates instances of class Agent with parameters specified.'''
        for squad in self.squad:
            for i in range(squad[1]):
                self.agent_list.append(Agent(squad[0],False))
                self.num_healthy += 1
            for i in range(squad[2]):
                self.agent_list.append(Agent(squad[0],True))
                self.num_infected += 1
        for i in range(self.num_medic):
            self.agent_list.append(Agent("Med", False))
            self.num_healthy += 1

    def x_range(self, role, new_x):
        '''Checks and returns x range within allowed range for squad'''
        for squad in self.squad:
            if role == squad[0]:
                if new_x < squad[3][0]:
                    new_x = squad[3][0]
                elif new_x > squad[3][1]:
                    new_x = squad[3][1]
            else:
                if new_x < 0: new_x = 0
                if new_x > self.board_size-1: new_x = self.board_size-1
            return new_x

    def x_movement(self, role, x):
        '''Generates new X coordinate based on a random integer'''
        rand = random.randint(0,8)
        new_x = x + ((rand % 3)-1)
        if new_x < 0: new_x = 0
        if new_x > self.board_size-1: new_x = self.board_size-1
        return new_x

    def y_range(self, role, new_y):
        '''Checks and returns y within y range for squad '''
        for squad in self.squad:
            if role == squad[0]:
                if new_y < squad[4][0]:
                    new_y = squad[4][0]
                elif new_y > squad[4][1]:
                    new_y = squad[4][1]
            else:
                if new_y < 0: new_y = 0
                if new_y > self.board_size-1: new_y = self.board_size-1
            return new_y


    def y_movement(self,role,y):
        '''Generates new Y coordinate based on random integer'''
        rand = random.randint(0,8)
        if rand <= 2 and rand >= 0:
            new_y = y + 1
        elif rand <= 5 and rand >= 3:
            new_y = y
        elif rand <= 8 and rand >= 6:
            new_y = y - 1

        return self.y_range(role,new_y)

    def tags(self):
        '''
        Generates a two dementional array representing the simulation board.
        Each entry contains a tag representing the position on the board.
        '''
        for i in range(self.board_size):
            self.board.append([])

        for i in range(len(self.board)-1, -1, -1):
            col = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T"]
            for n in col:
                n = n + str(i)
                self.board[i].append(n)

    def collision_check(self):
        '''
        Checks for collision between agents and preforms approprate event.
        Appends position tags of infected, healthy, and medics to respective list.
        Sets number of healthy and infected agents and checks for infection and recovery.
        '''
        self.infected_tag =[]
        self.healthy_tag = []
        self.medic_tag = []

        for agent in self.agent_list:
            if agent.state == True:
                self.infected_tag.append(agent.tag)
            elif agent.state == False:
                self.healthy_tag.append(agent.tag)
            if agent.role == "Med":
                self.medic_tag.append(agent.tag)
        self.num_healthy = len(self.healthy_tag)
        self.num_infected = len(self.infected_tag)
        for tag in self.infected_tag:
            if tag in self.healthy_tag:
                for agent in self.agent_list:
                    if agent.tag == tag and agent.state == False:
                        if random.random() <= self.infection_p:
                            agent.state = True
                            agent.infected_t = self.t
                            self.infection_cord.append([agent.x, agent.y])
                            self.infection_count += 1
                            self.num_healthy -= 1
                            self.num_infected += 1

            if tag in self.medic_tag:
                for agent in self.agent_list:
                    if agent.tag == tag and agent.state == True:
                        agent.state = False
                        agent.infected_t = 0
                        self.recovery_cord.append([agent.x,agent.y])
                        self.recovered_count += 1
                        self.num_healthy += 1
                        self.num_infected -= 1

    def natural_recovery(self):
        '''
        After a random amount of time with triangular distribution from user
        input, infected agents will become healthy again.
        '''
        for agent in self.agent_list:
            if agent.state == True:
                if self.t >= agent.infected_t + self.recovery_t:
                    agent.state = False
                    agent.infected_t = 0

    def generate_file(self, mode, *args):
        '''Generates data file with inputs'''
        with open('InfectionSim'+__version__+'.csv', mode) as file:
            writer = csv.writer(file)
            data = []
            for i in args:
                data.append(i)
            writer.writerow(data)

    def setup(self):
        screenSize = 800
        size(screenSize,screenSize)
        background(0)
        for i in range(0,screenSize):
            if i%40 == 0:
                stroke(255)
                line(0,i,screenSize,i)
                line(i,0,i,screenSize)

    def draw(self):
        c = 255/self.end_t
        for agent in self.agent_list:
            if agent.role == "Med":
                fill(0,self.t*c,0)
            elif agent.role == "A":
                fill(self.t*c,0,0)
            elif agent.role == "B":
                fill(0,0,self.t*c)
            rect(agent.x*40,agent.y*40,40,40)

    def run(self):
        '''
        Main method. Calls method to generate agents and board.
        Adds headers to the data output file.
        At every timestep, generates random movement and checks for collision.
        For every collision, infection occures at infection_p
        '''
        self.setup()
        self.generate_agents()
        self.tags()
        self.generate_file("w","Time","NumInfected","NumHealthy","NumMedic","NumRecovered","NumInfections")
        for self.t in range(0, self.end_t + 1):
            if self.t == 0:
                for agent in self.agent_list:
                    rx = random.randint(0,self.board_size-1)
                    ry = random.randint(0,self.board_size-1)
                    agent.x = rx
                    agent.y = ry
                    agent.tag = self.board[agent.x][agent.y]
                    #self.natural_recovery()
                    #print self.t, agent.role, agent.state, agent.tag, agent.x, agent.y
                self.generate_file('a',self.t,self.num_infected,self.num_healthy,self.num_medic)
                #print "Time: ", self.t, "# infected: ", self.num_infected, "# healthy: ", self.num_healthy
                self.draw()
                self.t += 1
            else:
                for agent in self.agent_list:
                    agent.x = self.x_movement(agent.role,agent.x)
                    agent.y = self.y_movement(agent.role,agent.y)
                    agent.tag = self.board[agent.x][agent.y]
                    self.natural_recovery()
                    #print self.t, agent.role, agent.state, agent.tag, agent.x, agent.y
                self.collision_check()
                self.generate_file('a',self.t,self.num_infected,self.num_healthy,self.num_medic,self.recovered_count,self.infection_count)
                #print "Time: ", self.t, "# infected: ", self.num_infected, "# healthy: ", self.num_healthy, "# recovered: ", self.recovered_count, "# infections: ", self.infection_count
                self.draw()
                self.t += 1


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
        self.infected_t = 0

### SQUAD PARAMETERS ###
# ["Role",#healthy, #infected]
squad1 = ["A", 4, 1,[0,9],[0,9]]
squad2 = ["B", 4, 1,[10,19],[10,19]]

### ENTER PARAMETERS ###
end_t = 10
num_medic = 1
infection_p = [0.3,0.9,0.5]
recovery_t = [48,120,72]
#########################
#random.seed(123)
InfectionSim(end_t,num_medic,infection_p,recovery_t,squad1,squad2).run()
