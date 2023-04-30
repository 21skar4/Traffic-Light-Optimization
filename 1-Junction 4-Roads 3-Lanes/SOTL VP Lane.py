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

    # define output file 


def run_simulation(Total_i,i,simulation_duration):
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
    T = 10.0
    phase_duration = 10.0 #intialize phase duration
    # get the time at the last point of traffic light change
    time = 0.0
    #to get total waiting time
    cumulative_waiting_time = 0.0
    count = 0
    #to store waiting time data
    waiting_time_data = [] 

    #to get last point of time when that edge was green
    E0_time = traci.simulation.getTime()
    E1_time = traci.simulation.getTime()
    E2_time = traci.simulation.getTime()
    E3_time = traci.simulation.getTime()

    # start the main loop
    while traci.simulation.getTime() < simulation_duration:  # end the iteration if simulation time is greater than simulation duration
        # get the current simulation time
        current_time = traci.simulation.getTime()
        Total_vehicles = 0 # total vehicles in the network at that time
        Total_waiting_time = 0.0 #total waiting time in the network at that time

        for lane in lanes:
          waiting_time_lane = traci.lane.getWaitingTime(lane) #waiting time at that lane
          waiting_vehicles_number = traci.lane.getLastStepVehicleNumber(lane) #number of vehicles at that lane
          Total_waiting_time = Total_waiting_time +  waiting_time_lane
          Total_vehicles = Total_vehicles + waiting_vehicles_number
         
        waiting_time_data.append(Total_waiting_time)
    
        cumulative_waiting_time += Total_waiting_time
        count +=1
        # switch the traffic light state based on the current time
        if current_time - (time + phase_duration) > traci.simulation.getDeltaT():

            # if total waiting time or total vehilce is zero then apply fixed time algorithm
            if Total_waiting_time == 0 or Total_vehicles ==0:
                # Fixed Time algorithm 
            
                if current_time - E0_time == 40 or E0_time == 0:
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E0)
                    E0_time = traci.simulation.getTime() # to get time when the traffic was green for this lane

                elif current_time - E1_time == 40 or E1_time == 10:
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E1 )
                    E1_time = traci.simulation.getTime() # to get time when the traffic was green for this lane

                elif current_time - E2_time == 40 or E2_time== 20:
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E2 )
                    E2_time = traci.simulation.getTime() # to get time when the traffic was green for this lane

                elif current_time - E3_time == 40 or E3_time == 30:
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E3 )
                    E3_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                
                
                phase_duration = 10.0

                # get the time at last point of traffic light change
                time = traci.simulation.getTime()

            else:   
                # our main algorithm  

                most_conjested_lane = None
                highest_traffic_value = 0.0 # our decesion making parameter
                #normalized values 
                normalized_waiting_time = 0.0 
                normalized_waiting_vehicles = 0.0
                total_traffic_value = 0.0
                for lane in lanes:
                    waiting_time_lane = traci.lane.getWaitingTime(lane)
                    waiting_vehicles_number = traci.lane.getLastStepVehicleNumber(lane)
                    normalized_waiting_time = waiting_time_lane / Total_waiting_time
                    normalized_waiting_vehicles = waiting_vehicles_number/Total_vehicles
                    traffic_value = pow(normalized_waiting_time,(1-(i/(Total_i))))*pow(normalized_waiting_vehicles,i/(Total_i))
                    total_traffic_value+=traffic_value
                    #get the highest traffic value and corresponding lane
                    if traffic_value > highest_traffic_value:
                        highest_traffic_value = traffic_value
                        most_conjested_lane = lane 
                
                if  most_conjested_lane == "-E0_0" or  most_conjested_lane == "-E0_1" or most_conjested_lane == "-E0_2":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E0 )
                    E0_time = traci.simulation.getTime() # to get time when the traffic was green for this edge

                if most_conjested_lane == "-E1_0" or  most_conjested_lane == "-E1_1" or  most_conjested_lane == "-E1_2":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E1 )
                    E1_time = traci.simulation.getTime() # to get time when the traffic was green for this edge

                if most_conjested_lane == "-E2_0" or most_conjested_lane == "-E2_1" or  most_conjested_lane == "-E2_2":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E2 )
                    E2_time = traci.simulation.getTime() # to get time when the traffic was green for this edge

                if most_conjested_lane == "-E3_0" or most_conjested_lane == "-E3_1" or most_conjested_lane == "-E3_2":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E3 )
                    E3_time = traci.simulation.getTime() # to get time when the traffic was green for this edge

                #get new phase duration
                phase_duration = highest_traffic_value*T/total_traffic_value

                # get the time at the last point of traffic light change
                time = traci.simulation.getTime()

            # advance the simulation
        traci.simulationStep()
        
    Average_Waiting_Time = cumulative_waiting_time/count
    traci.close()    
    sys.stdout.flush()
    print(Average_Waiting_Time)
    return waiting_time_data

    

if __name__ == "__main__":
    options = get_options()
    # check binary
    sumoBinary = checkBinary('sumo')    
    # traci starts sumo as a subprocess and then this script connects and runs
    config_file = os.path.join("E:\ME308 Project\Test7", "SUMO Configuration.sumocfg")
    traffic_scale = 0.6
    simulation_duration = 3100
    Total_i = 20
    data = np.zeros((simulation_duration,Total_i+1))
    for i in range(Total_i+1): # Run 10 simulations
        print(i)
        sumo_cmd = [sumoBinary, "-c", config_file,"--no-warnings",f'--scale={traffic_scale}',"--start","--quit-on-end"]
        traci.start(sumo_cmd)
        m = run_simulation(Total_i,i,simulation_duration)
        data[:,i] = m
np.savetxt(f"SOTL VP Lane.csv",data)

# Plot each column of data with a different color
fig, ax = plt.subplots()
for i in range(Total_i+1):
    ax.plot(data[:, i], label=f'Iteration {i}')

# Set the axis labels and title
ax.set_xlabel('Simulation Time')
ax.set_ylabel('Waiting Time')
ax.set_title('Waiting Time Vs Simulation Time')
# Add a legend
ax.legend()

# save the plot
plt.savefig('Waiting Time Vs Simulation Time SOTL VP Lane.png')

# Show the plot
plt.show()