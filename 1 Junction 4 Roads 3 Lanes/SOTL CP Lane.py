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
    phase_duration = 10.0
    Average_Waiting_Time = 0.0
    waiting_time_data = [] #to store waiting time data 
    #cumulative waiting time for each lane
    l1_cumulative_waiting_time = 0.0
    l2_cumulative_waiting_time = 0.0
    l3_cumulative_waiting_time = 0.0
    l4_cumulative_waiting_time = 0.0
    l5_cumulative_waiting_time = 0.0
    l6_cumulative_waiting_time = 0.0
    l7_cumulative_waiting_time = 0.0
    l8_cumulative_waiting_time = 0.0
    l9_cumulative_waiting_time = 0.0
    l10_cumulative_waiting_time = 0.0
    l11_cumulative_waiting_time = 0.0
    l12_cumulative_waiting_time = 0.0    

    # start the main loop
    while traci.simulation.getTime() < simulation_duration:  # end the iteration if simulation time is grater than simulation_duration
        # get the current simulation time
        current_time = traci.simulation.getTime()        
        Total_vehicles = 0
        Total_waiting_time = 0.0
        for lane in lanes:
                waiting_time = traci.lane.getWaitingTime(lane)
                #get and add waiting time to its corresponding lanes                
                if lane == '-E0_0':
                   l1_cumulative_waiting_time+=waiting_time
                elif lane == '-E0_1':
                   l2_cumulative_waiting_time+=waiting_time
                elif lane == '-E0_2':
                   l3_cumulative_waiting_time+=waiting_time
                elif lane == '-E1_0':
                   l4_cumulative_waiting_time+=waiting_time
                elif lane == '-E1_1':
                   l5_cumulative_waiting_time+=waiting_time
                elif lane == '-E1_2':
                   l6_cumulative_waiting_time+=waiting_time
                elif lane == '-E2_0':
                   l7_cumulative_waiting_time+=waiting_time
                elif lane == '-E2_1':
                   l8_cumulative_waiting_time+=waiting_time
                elif lane == '-E2_2':
                   l9_cumulative_waiting_time+=waiting_time
                elif lane == '-E3_0':
                   l10_cumulative_waiting_time+=waiting_time
                elif lane == '-E3_1':
                   l11_cumulative_waiting_time+=waiting_time
                elif lane == '-E3_2':
                   l12_cumulative_waiting_time+=waiting_time
        #get the total waiting time and number of vehicles in the network at that moment
        for lane in lanes:
          waiting_time_lane = traci.lane.getWaitingTime(lane)
          waiting_vehicles_number = traci.lane.getLastStepVehicleNumber(lane)
          Total_waiting_time = Total_waiting_time + waiting_time_lane
          Total_vehicles = Total_vehicles + waiting_vehicles_number
         
        waiting_time_data.append(Total_waiting_time)

        if current_time % phase_duration==0:  #update at a constant phase duration 
            most_conjested_lane = None #lane with highest traffic value
            highest_traffic_value = 0.0 # our decesion making parameter

            #normalized waiting time and number of vehicles
            normalized_waiting_time = 0.0 
            normalized_waiting_vehicles = 0.0

            # if total waiting time or total vehilce is zero then apply fixed time algorithm
            a =0
            if Total_waiting_time == 0 or Total_vehicles ==0:
                # Fixed Time algorithm            
                if a == 0:
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E0 )   
                    a =1               
                elif a == 1:
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E1 )
                    a = 2
                elif a == 2:
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E2 )
                    a = 3
                elif a == 3:
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E3 )
                    a = 0
               
            else:   
                # our SOTL algorithm  
                for lane in lanes:
                    waiting_time_lane = traci.lane.getWaitingTime(lane) #get waiting time in that lane
                    waiting_vehicles_number = traci.lane.getLastStepVehicleNumber(lane) #get number of vehicles in that lane
                    normalized_waiting_time = waiting_time_lane / Total_waiting_time
                    normalized_waiting_vehicles = waiting_vehicles_number/Total_vehicles
                    # give some mathematical function to the "traffic_value"
                    traffic_value = pow(normalized_waiting_time,(1-(i/(Total_i))))*pow(normalized_waiting_vehicles,i/(Total_i))
                    if traffic_value > highest_traffic_value:
                        highest_traffic_value = traffic_value
                        most_conjested_lane = lane 
                
                if  most_conjested_lane == "-E0_0":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E0 )
                    E0_time = traci.simulation.getTime() # to get time when the traffic was green for this lane

                if most_conjested_lane == "-E1_0":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E1 )
                    E1_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                
                if most_conjested_lane == "-E2_0":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E2 )
                    E2_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
        
                if most_conjested_lane == "-E3_0":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E3 )
                    E3_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                    
                
            

            # advance the simulation
        traci.simulationStep()
        
    Average_Waiting_Time = np.average(waiting_time_data)

    #print(Average_Waiting_Time)
    traci.close()    
    lane_waiting_values = [l1_cumulative_waiting_time,l2_cumulative_waiting_time,l3_cumulative_waiting_time,l4_cumulative_waiting_time,l5_cumulative_waiting_time,l6_cumulative_waiting_time,l7_cumulative_waiting_time,l8_cumulative_waiting_time, l9_cumulative_waiting_time,l10_cumulative_waiting_time,l11_cumulative_waiting_time,l12_cumulative_waiting_time]
    max_lane = np.argmax(lane_waiting_values)
    max_lane_value = np.amax(lane_waiting_values)
    sum_lane = np.sum(lane_waiting_values)
    sys.stdout.flush()
    print(max_lane,max_lane_value,sum_lane)
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
    Total_i = 2
    data = np.zeros((simulation_duration,Total_i+1))
    for i in range(Total_i+1): # Run 10 simulations
        print(i)
        sumo_cmd = [sumoBinary, "-c", config_file,"--no-warnings",f'--scale={traffic_scale}',"--start","--quit-on-end"]
        traci.start(sumo_cmd)
        m = run_simulation(Total_i,i,simulation_duration)
        data[:,i] = m
np.savetxt(f"SOTL CP Lane.csv",data)

#ploting graphs for Waiting Time Vs Simulation Time
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
plt.savefig('Waiting Time Vs Simulation Time SOTL CP Lane.png')

# Show the plot
plt.show()