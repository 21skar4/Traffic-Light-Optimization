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

def run_simulation(i,simulation_duration,total_i):
    # define the junction ID
    junction_id = "J5"
    lanes = traci.lane.getIDList()

    # define the state strings for the traffic lights
    north_to_west_and_east_state = "GGrrrr"
    east_to_north_and_west_state = "rrGGrr"
    west_to_east_and_north_state = "rrrrGG"
   
    T = 10.0
    phase_duration = 0.0 
    time = 0.0
    #to get total waiting time
    Cumulative_waiting_time = 0.0
    #to store waitng time data
    waiting_time_data = []
    
    # start the main loop
    while traci.simulation.getTime() < simulation_duration:  # end the iteration if time is greater than simulation duration
        # get the current simulation time
        current_time = traci.simulation.getTime()
        
        Total_vehicles = 0 #total number of vehicles in the network
        Total_waiting_time = 0.0 #total waiting time in the network
        for lane in lanes:
            waiting_time_lane0 = traci.lane.getWaitingTime(lane) #waiting time in the lane
            waiting_vehicles_number0 = traci.lane.getLastStepVehicleNumber(lane) #number of vehicles in that lane
            Total_waiting_time = Total_waiting_time + waiting_time_lane0
            Total_vehicles = Total_vehicles + waiting_vehicles_number0
        Cumulative_waiting_time += Total_waiting_time    
        waiting_time_data.append(Total_waiting_time)    
        # switch the traffic light state based on the current time
        if current_time - (time + phase_duration) > traci.simulation.getDeltaT():

                # main algorithm
                # if total waiting time or total vehilce is zero then apply fixed time algorithm or randomly assign traffic light
                if Total_waiting_time == 0.0 or Total_vehicles == 0:
                    traci.trafficlight.setRedYellowGreenState(junction_id, north_to_west_and_east_state)
                    time = traci.simulation.getTime()
                    phase_duration = 5 
                else:
                    #normalized values
                    normalized_waiting_time = 0.0
                    normalized_waiting_vehicles = 0.0
                    total_traffic_value = 0
                    most_conjested_lane = None
                    highest_traffic_value = 0.0
                    for lane in lanes:
                        waiting_time_lane = traci.lane.getWaitingTime(lane)
                        waiting_vehicles_number = traci.lane.getLastStepVehicleNumber(lane)
                        normalized_waiting_time = waiting_time_lane/Total_waiting_time
                        normalized_waiting_vehicles = waiting_vehicles_number/Total_vehicles
                        traffic_value = pow(normalized_waiting_time,(1-(i/total_i)))*pow(normalized_waiting_vehicles,i/total_i)
                        total_traffic_value+=traffic_value
                        #get highest traffic_value by comparing different lanes
                        if traffic_value > highest_traffic_value:
                            highest_traffic_value = traffic_value
                            most_conjested_lane = lane
                    
                    if most_conjested_lane == "-E1_0":
                        traci.trafficlight.setRedYellowGreenState(junction_id, north_to_west_and_east_state) #chnage traffic state
                    if most_conjested_lane == "-E2_0":
                        traci.trafficlight.setRedYellowGreenState(junction_id, west_to_east_and_north_state)
                    if most_conjested_lane== "-E3_0":
                        traci.trafficlight.setRedYellowGreenState(junction_id, east_to_north_and_west_state)
                    #change phase duration
                    phase_duration = highest_traffic_value*T/total_traffic_value
                    # get the current simulation time
                    time = traci.simulation.getTime()        
        # advance the simulation
        traci.simulationStep()
          
    traci.close()
    sys.stdout.flush()

    Average_waiting_time = Cumulative_waiting_time/simulation_duration
    print(f"Average waiting time\t{Average_waiting_time}")
    return waiting_time_data


if __name__ == "__main__":
    options = get_options()
    # check binary
    sumoBinary = checkBinary('sumo')    
    # traci starts sumo as a subprocess and then this script connects and runs
    config_file = os.path.join("E:\ME308 Project\Test5", "SUMO Configuration.sumocfg")
    traffic_scale = 0.6
    simulation_duration = 3100
    total_i = 20
    data = np.zeros((simulation_duration,total_i+1))
    for i in range(total_i+1): # Run 10 simulations
        print(i)
        sumo_cmd = [sumoBinary, "-c", config_file,"--no-warnings",f'--scale={traffic_scale}',"--start","--quit-on-end"]
        traci.start(sumo_cmd)
        m = run_simulation(i,simulation_duration,total_i)
        data[:,i] = m
np.savetxt(f"SOTL VP.csv",data)

# Create a new figure and axis object
fig, ax = plt.subplots()

# Plot each column of data with a different color
for i in range(total_i+1):
    ax.plot(data[:, i], label=f'Iteration {i}')

# Set the axis labels and title
ax.set_xlabel('Simulation Time')
ax.set_ylabel('Waiting Time')
ax.set_title('Waiting Time Vs Simulation Time')
# Add a legend
ax.legend()

# save the plot
plt.savefig('Waiting Time Vs Simulation Time SOTL VP.png')

# Show the plot
plt.show()
        
       