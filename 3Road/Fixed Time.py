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
    junction_id = "J5"

    lanes = traci.lane.getIDList()

    # define the state strings for the traffic lights
    north_to_west_and_east_state = "GGrrrr"
    east_to_north_and_west_state = "rrGGrr"
    west_to_east_and_north_state = "rrrrGG"

    # set the initial state for the traffic lights
    #traci.trafficlight.setRedYellowGreenState("J5", north_to_west_state + north_to_east_state + east_to_west_state + east_to_north_state + west_to_east_state + west_to_north_state)

    # define the duration of each phase
    phase_duration = 10
    a = 0
    waiting_time_data = []
    # start the main loop
    while traci.simulation.getTime() < simulation_duration:
        
        Total_waiting_time = 0.0
        for lane in lanes:
            waiting_time_lane = traci.lane.getWaitingTime(lane)
            
            Total_waiting_time = Total_waiting_time + waiting_time_lane
            
          
        waiting_time_data.append(Total_waiting_time)  
        # get the current simulation time
        current_time = traci.simulation.getTime()
        
        # switch the traffic light state based on the current time
        if current_time % phase_duration == 0:
        
            if a ==0 :
                traci.trafficlight.setRedYellowGreenState(junction_id, north_to_west_and_east_state)
                a=1
            elif a ==1:
                traci.trafficlight.setRedYellowGreenState(junction_id, west_to_east_and_north_state)
                a=2
            elif a==2:
                traci.trafficlight.setRedYellowGreenState(junction_id, east_to_north_and_west_state)
                a=0

        # advance the simulation
        traci.simulationStep()

    traci.close()
    sys.stdout.flush()
    return waiting_time_data


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
    config_file = os.path.join("E:\ME308 Project\Test5", "SUMO Configuration.sumocfg")
    sumo_cmd = [sumoBinary, "-c", config_file,f'--scale={traffic_scale}',"--start","--quit-on-end"] #remove "--start" and "--quit-on-end" if you want to start and end simulation manually
    traci.start(sumo_cmd)
    m=run(simulation_duration)
    print("Average Waiting Time",np.average(m))
    np.savetxt("Fixed Time.csv",m)


# Create a new figure and axis object
fig, ax = plt.subplots()

# Plot each column of data with a different color

ax.plot(m, label=f'Fixed Time')

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
