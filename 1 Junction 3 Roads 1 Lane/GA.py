#!/usr/bin/env python

import os
import sys
import optparse
import random

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'C:/Program Files (x86)/Eclipse/Sumo/tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # Checks for the binary in environ vars
import traci

def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

# main entry point
if __name__ == "__main__":
    options = get_options()

    sumo_binary = checkBinary('sumo')
    sumo_binary_gui = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    config_file = os.path.join("C:/Users/Sashr/OneDrive/Documents/ME 308 Project", "SUMO Configuration.sumocfg")
    sumo_cmd = [sumo_binary, "-c", config_file, "--no-warnings"]
    sumo_cmd_gui = [sumo_binary_gui, "-c", config_file]

# Non calibratable variables
simulation_duration = 1000
characters = ['G', 'r']
string_length = 6

# Calibratable variables
population_size = 6
crossover_rate = 0.1
mutation_rate = 0.1
generations = 5
steps = 200
STEPS = 10

def fitness_function(traffic_state):
    waiting_time = 0

    traci.start(sumo_cmd, label = "simulation_2")
    traci.switch("simulation_2")
    traci.simulation.loadState("simulation_state.xml.gz")
    traci.trafficlight.setRedYellowGreenState("J5", traffic_state)

    # Run the auxiliary simulation for steps steps
    for i in range(steps):
        traci.simulationStep()

    for lane in traci.lane.getIDList():
        waiting_time = waiting_time + traci.lane.getWaitingTime(lane)
    
    traci.close()
    
    return waiting_time

traci.start(sumo_cmd_gui, label = "simulation_1")
traci.switch("simulation_1")

while traci.simulation.getTime() < simulation_duration:
    traci.simulation.saveState("simulation_state.xml.gz")

    # Generate the initial population of traffic states
    traffic_states = []
    fitness_scores = []
    for i in range(population_size):
        traffic_state = ''.join(random.choices(characters, k = string_length))
        traffic_states.append(traffic_state)
        fitness_scores.append(fitness_function(traffic_state))
    
    # Select the best traffic states
    best_traffic_states = []
    for i in range(int(population_size/2)):
        best_traffic_state = traffic_states[fitness_scores.index(min(fitness_scores))]
        best_traffic_states.append(best_traffic_state)
        traffic_states.remove(best_traffic_state)
        fitness_scores.remove(min(fitness_scores))
    
    for generation in range(generations):
        print("Generation: ", generation)
        new_traffic_states = []

        # Perform crossover and mutation
        while len(new_traffic_states) < population_size:
            parent_1 = random.choice(best_traffic_states)
            parent_2 = random.choice(best_traffic_states)

            if random.uniform(0, 1) < crossover_rate:
                crossover_point = random.randint(1, string_length - 1)
                child_1 = parent_1[:crossover_point] + parent_2[crossover_point:]
                child_2 = parent_2[:crossover_point] + parent_1[crossover_point:]
            else:
                child_1 = parent_1
                child_2 = parent_2
            
            if random.uniform(0, 1) < mutation_rate:
                mutation_point = random.randint(0, string_length - 1)
                if child_1[mutation_point] == 'G':
                    child_1 = child_1[:mutation_point] + 'r' + child_1[mutation_point + 1:]
                else:
                    child_1 = child_1[:mutation_point] + 'G' + child_1[mutation_point + 1:]
            
            if random.uniform(0, 1) < mutation_rate:
                mutation_point = random.randint(0, string_length - 1)
                if child_2[mutation_point] == 'G':
                    child_2 = child_2[:mutation_point] + 'r' + child_2[mutation_point + 1:]
                else:
                    child_1 = child_1[:mutation_point] + 'G' + child_1[mutation_point + 1:]
            
            new_traffic_states.append(child_1)
            new_traffic_states.append(child_2)
        
        best_traffic_states = new_traffic_states
        print(best_traffic_states)

    new_fitness_scores = []
    for traffic_state in best_traffic_states:
        new_fitness_scores.append(fitness_function(traffic_state))
    
    optimum_traffic_state = best_traffic_states[new_fitness_scores.index(min(new_fitness_scores))]
    
    print(optimum_traffic_state)

    traci.switch("simulation_1")

    traci.trafficlight.setRedYellowGreenState("J5", optimum_traffic_state)

    # Run the main simulation for STEPS steps
    for i in range(STEPS):
        traci.simulationStep()

traci.close()