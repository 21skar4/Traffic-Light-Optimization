#!/usr/bin/env python

import os
import sys
import optparse
import numpy as np
import matplotlib.pyplot as plt

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'C:\Program Files (x86)\Eclipse\Sumo\tools')
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


def run(simulation_duration):
    # main simulation loop
    # define the junction ID
    junction_id = "J0"
    lanes = traci.lane.getIDList()

    # define the state strings for the traffic lights
    #for edge "-E0"
    neg_E0 = "GGGGGrrrrrrrrrrrrrrr"
    
    #for edge "-E1"
    neg_E1 = "rrrrrGGGGGrrrrrrrrrr"
    
    #for edge "-E2"
    neg_E2 = "rrrrrrrrrrGGGGGrrrrr"
    
    #for edge "-E3"
    neg_E3 = "rrrrrrrrrrrrrrrGGGGG"
    
    # define the duration of each phase
    phase_duration = 10
    #to store waiting time data
    waiting_time_data = []

    while traci.simulation.getTime() < simulation_duration:
            
            # get the current simulation time
            current_time = traci.simulation.getTime()
            total_waiting_time = 0 #waitng time over the network at that time
            for lane in lanes:
                waiting_time = traci.lane.getWaitingTime(lane) #waiting time at that lane
                total_waiting_time = total_waiting_time + waiting_time

            waiting_time_data.append(total_waiting_time)

            # switch the traffic light state based on the current time
            if current_time % phase_duration == 0:
                max_waiting_cars = 0
                max_waiting_lane = None
                for lane in lanes:
                    waiting_cars = traci.lane.getLastStepVehicleNumber(lane)
                    if waiting_cars > max_waiting_cars:
                        max_waiting_cars = waiting_cars
                        max_waiting_lane = lane
                if max_waiting_lane == "-E0_0" or max_waiting_lane == "-E0_1" or max_waiting_lane == "-E0_2":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E0 ) #state change of traffic light
                
                if max_waiting_lane == "-E1_0" or max_waiting_lane == "-E1_1" or max_waiting_lane == "-E1_2":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E1 )
               
                if max_waiting_lane == "-E2_0" or max_waiting_lane == "-E2_1" or max_waiting_lane == "-E2_2":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E2 )
                
                if max_waiting_lane == "-E3_0" or max_waiting_lane == "-E3_1" or max_waiting_lane ==  "-E3_2":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E3 )
               
            # advance the simulation
            traci.simulationStep()

    traci.close()
    sys.stdout.flush()
    return  waiting_time_data
        
# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    simulation_duration = 3100
    traffic_scale = 0.6
    config_file = os.path.join("E:\ME308 Project\Test7", "SUMO Configuration.sumocfg")
    sumo_cmd = [sumoBinary, "-c", config_file,'--no-warnings',f'--scale={traffic_scale}','--start','--quit-on-end']
    traci.start(sumo_cmd)
    m=run(simulation_duration)
    print(np.average(m))
    np.savetxt("MP CP Lane.csv",m)


#ploting graphs for Waiting Time Vs Simulation Time
fig, ax = plt.subplots()
ax.plot(m, label=f'MP CP Lane')

# Set the axis labels and title
ax.set_xlabel('Simulation Time')
ax.set_ylabel('Waiting Time')
ax.set_title('Waiting Time Vs Simulation Time')
# Add a legend
ax.legend()

# save the plot
plt.savefig('Waiting Time Vs Simulation MP CP Lane.png')

# Show the plot
plt.show()