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
def run(simulation_duration):
    # define the junction ID
    junction_id = "J5"
    lanes = traci.lane.getIDList()

    # define the state strings for the traffic lights
    north_to_west_and_east_state = "GGrrrr"
    east_to_north_and_west_state = "rrGGrr"
    west_to_east_and_north_state = "rrrrGG"
    NWE_time = 0
    WEN_time = 0
    ENW_time = 0
   
    # define the duration of each phase
    phase_duration = 10
    #to calculate total waiting time
    cumulative_waiting_time = 0.0
    #to store the waiting time data per second
    waiting_time_data = []
    # start the main loop
    while traci.simulation.getTime() < simulation_duration:  # end the iteration if time is greaater than time of simulation 
            # get the current simulation time
            current_time = traci.simulation.getTime()
            Total_vehicles = 0
            Total_waiting_time = 0.0
            
            for lane in lanes:
                waiting_time_lane = traci.lane.getWaitingTime(lane) # waiting time for the corresponding lane  
                waiting_vehicles_number = traci.lane.getLastStepVehicleNumber(lane) # number of vehicles for the corresponding lane  
                Total_waiting_time = Total_waiting_time +  waiting_time_lane # waiting time for the network at that time
                Total_vehicles = Total_vehicles + waiting_vehicles_number #number of vehicle for the network at that time
            cumulative_waiting_time += Total_waiting_time   
            waiting_time_data.append(Total_waiting_time)   
            # switch the traffic light state based on the current time 
            if current_time % phase_duration == 0:

                # if total waiting time or total vehilce is zero then apply fixed time algorithm
                if Total_waiting_time == 0 or Total_vehicles ==0:
                    # Fixed Time algorithm 
                    if current_time - NWE_time == 30 or NWE_time == 0:
                        traci.trafficlight.setRedYellowGreenState(junction_id, north_to_west_and_east_state)
                        
                        NWE_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                    elif current_time -WEN_time == 30 or ENW_time == 10 :
                        traci.trafficlight.setRedYellowGreenState(junction_id, west_to_east_and_north_state)
                        
                        WEN_time = traci.simulation.getTime() 
                    elif current_time - ENW_time == 30 or ENW_time == 20 :
                        traci.trafficlight.setRedYellowGreenState(junction_id, east_to_north_and_west_state)
                        
                        ENW_time = traci.simulation.getTime() 


                else:   
                 # our main algorithm  
                 most_conjested_lane = None 
                 highest_traffic_value = 0.0 # our decesion making parameter

                 #normalized values 
                 normalized_waiting_vehicles = 0.0
                 for lane in lanes:
                     waiting_vehicles_number = traci.lane.getLastStepVehicleNumber(lane)
                     normalized_waiting_vehicles = waiting_vehicles_number/Total_vehicles
                     traffic_value = normalized_waiting_vehicles
                     #get the highest traffic value and corresponding most conjested lane
                     if traffic_value > highest_traffic_value:
                         highest_traffic_value = traffic_value
                         most_conjested_lane = lane 
                 if most_conjested_lane == "-E1_0":
                    traci.trafficlight.setRedYellowGreenState(junction_id, north_to_west_and_east_state)
                    
                    NWE_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                 if most_conjested_lane == "-E2_0":
                    traci.trafficlight.setRedYellowGreenState(junction_id, west_to_east_and_north_state)
                  
                    WEN_time = traci.simulation.getTime()
                 if most_conjested_lane== "-E3_0":
                    traci.trafficlight.setRedYellowGreenState(junction_id, east_to_north_and_west_state)
                    
                    ENW_time = traci.simulation.getTime()

            # advance the simulation
            traci.simulationStep()
                
    Average_waiting_time = cumulative_waiting_time/simulation_duration
    
    traci.close()
    sys.stdout.flush()
    print(f"Average waiting time\t{Average_waiting_time}")
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
    sumo_cmd = [sumoBinary, "-c", config_file,"--no-warnings",f'--scale={traffic_scale}',"--start","--quit-on-end"] #remove "--start" and "--quit-on-end" if you want to start and end simulation manually
    traci.start(sumo_cmd)
    m=run(simulation_duration)
    np.savetxt("MP CP.csv",m)

#ploting graphs for Waiting Time Vs Simulation Time
fig, ax = plt.subplots()
ax.plot(m, label=f'MP CP')

# Set the axis labels and title
ax.set_xlabel('Simulation Time')
ax.set_ylabel('Waiting Time')
ax.set_title('Waiting Time Vs Simulation Time')
# Add a legend
ax.legend()

# save the plot
plt.savefig('Waiting Time Vs Simulation MP CP.png')

# Show the plot
plt.show()