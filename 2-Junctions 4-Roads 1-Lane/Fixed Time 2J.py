#!/usr/bin/env python

import os
import sys
import optparse
from sumolib import checkBinary
import traci
import numpy as np
import matplotlib.pyplot as plt

def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

def run_simulation(simulation_duration):
    # main simulation loop
    # define the junction ID
    junction_id1 = "J2"
    junction_id2 = "J3"


    lane1 = ['E0_0','-E4_0','-E3_0','-E1_0'] #left lanes
    lane2 = ['E1_0','-E5_0','-E2_0','-E6_0'] #right lanes
    

    # define the duration of each phase
    phase_duration = 10
    lane_length = traci.lane.getLength('E1_0')
    print("Length of middle lane",lane_length)
    network_waiting_time_list = [] #list for storing waiting time per step of simulation
    a=0
    
    while traci.simulation.getTime() < simulation_duration:
            # get the current simulation time
            current_time = traci.simulation.getTime() #simulation time at that point of simulation
            state = "GGGrrrrrrrrrrrrrrrrrrrrr" 
            total_waiting_time1 = 0 #total waiting time over all the edges in the left junction 
            total_waiting_time2 = 0  #total waiting time over all the edges in the left junction
            
            for lane in lane1:
                    waiting_time_lane1 = traci.lane.getWaitingTime(lane)    # waiting time for the corresponding lane                               
                    total_waiting_time1 += waiting_time_lane1
                   
            for lane in lane2:                   
                    waiting_time_lane2 = traci.lane.getWaitingTime(lane)    # waiting time for the corresponding lane                               
                    total_waiting_time2 += waiting_time_lane2

            network_waiting_time = total_waiting_time1+total_waiting_time2 #total waiting time over the whole network
            network_waiting_time_list.append(network_waiting_time)
           
            # switch the traffic light state based on the current time
            if current_time % phase_duration == 0:
                if a ==0:
                     state='GGGrrrrrrrrrrrrrrrrrrrrr' #North_edge_left_junction
                     a=1
                elif a ==1:
                     state = 'rrrGGGrrrrrrrrrrrrrrrGGG' #Middle edges
                     a=2
                elif a ==2:
                     state='rrrrrrGGGrrrrrrrrrrrrrrr'  #South_edges_left_junction
                     a=3
                elif a ==3:
                     state='rrrrrrrrrGGGrrrrrrrrrrrr' #West_edges_left_junction
                     a=4
                elif a ==4:
                     state='rrrrrrrrrrrrGGGrrrrrrrrr' #North_edges_right_junction
                     a=5
                elif a ==5:
                     state='rrrrrrrrrrrrrrrGGGrrrrrr' #East_edges_right_junction
                     a=6
                elif a==6:
                     state='rrrrrrrrrrrrrrrrrrGGGrrr' #South_edges_right_junction
                     a=0

                
                traci.trafficlight.setRedYellowGreenState(junction_id2, state ) #change state of traffic light to "state"
                    

            traci.simulationStep() #go on to the next step

    traci.close()
    sys.stdout.flush()
    average_waiting_time = np.average(network_waiting_time_list)
    print("Average Waiting Time",average_waiting_time)
    return network_waiting_time_list



if __name__ == "__main__":
    options = get_options()

    # check binary
    sumoBinary = checkBinary('sumo-gui')    
    # traci starts sumo as a subprocess and then this script connects and runs
    config_file = os.path.join("E:\ME308 Project\Test8", "Configuration.sumocfg")
    traffic_scale = 0.6
    simulation_duration = 3100
    sumo_cmd = [sumoBinary, "-c", config_file, "--no-warnings",f'--scale={traffic_scale}',"--start", "--quit-on-end"]
    traci.start(sumo_cmd)
    n=run_simulation(simulation_duration)
    np.savetxt('Fixed Time 2J.csv',n) 

#ploting graphs for Waiting Time Vs Simulation Time
fig, ax = plt.subplots()
ax.plot(n, label=f'Fixed Time')

# Set the axis labels and title
ax.set_xlabel('Simulation Time')
ax.set_ylabel('Waiting Time')
ax.set_title('Waiting Time Vs Simulation Time')
# Add a legend
ax.legend()

# save the plot
plt.savefig('Waiting Time Vs Simulation Fixed Time.png')

# Show the plot
plt.show()