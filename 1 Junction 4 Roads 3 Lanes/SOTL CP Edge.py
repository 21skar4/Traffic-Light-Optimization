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
    edges = traci.edge.getIDList()
 

    # define the state strings for the traffic lights
    #for lane "-E0_"
    neg_E0 = "GGGGGrrrrrrrrrrrrrrr"
    #neg_E0_ ="North" 
    
    #for lane "-E1_"
    neg_E1 = "rrrrrGGGGGrrrrrrrrrr"
    neg_E1_ ="East" 
    
    
    #for lane "-E2_0"
    neg_E2 = "rrrrrrrrrrGGGGGrrrrr"
    neg_E2_ ="South" 
    

    #for lane "-E3_"
    neg_E3 = "rrrrrrrrrrrrrrrGGGGG"
    neg_E3_ ="West" 
    


    # set the initial state for the traffic lights
    #traci.trafficlight.setRedYellowGreenState("J5", north_to_west_state + north_to_east_state + east_to_west_state + east_to_north_state + west_to_east_state + west_to_north_state)

    # define the duration of each phase
    T = 10.0
    phase_duration = 0.0 #or T
    time = 0.0
    cumulative_waiting_time = 0.0
    Average_Waiting_Time = 0.0
    count = 0
    waiting_time_data = []
    
    prev_time = 0.0
    # start the main loop
    E0_time = traci.simulation.getTime()
    E1_time = traci.simulation.getTime()
    E2_time = traci.simulation.getTime()
    E3_time = traci.simulation.getTime()
    while traci.simulation.getTime() < simulation_duration:  # end the iteration if sim_time is greater than 200
        # get the current simulation time
        current_time = traci.simulation.getTime()
        
        Total_vehicles = 0
        Total_waiting_time = 0.0
        for edge in edges:
          waiting_time_edge = traci.edge.getWaitingTime(edge)
          waiting_vehicles_number = traci.edge.getLastStepVehicleNumber(edge)
          Total_waiting_time = Total_waiting_time + waiting_time_edge
          Total_vehicles = Total_vehicles + waiting_vehicles_number
         
        waiting_time_data.append(Total_waiting_time)
    
        cumulative_waiting_time += Total_waiting_time
        count +=1
        l=10
        # switch the traffic light state based on the current time
        #if current_time - (time + phase_duration) > traci.simulation.getDeltaT(): #for varying phase
        if current_time % l==0:  #for constant phase
            most_conjested_edge = None
            highest_traffic_value = 0.0 # our decesion making parameter

            #normalized values 
            normalized_waiting_time = 0.0 
            normalized_waiting_vehicles = 0.0

            # if total waiting time or total vehilce is zero then apply fixed time algorithm
            if Total_waiting_time == 0 or Total_vehicles ==0:
                # Fixed Time algorithm 
            
                if current_time - E0_time == 40 or E0_time == 0:
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E0 )
                   # f.write(f"{current_time}\t{neg_E0_0}\t{neg_E0_0_}\n")
                    E0_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                elif current_time - E1_time == 40 or E1_time == 10:
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E1 )
                   # f.write(f"{current_time}\t{neg_E1_0}\t{neg_E1_0_}\n")
                    E1_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                elif current_time - E2_time == 40 or E2_time== 20:
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E2 )
                   # f.write(f"{current_time}\t{neg_E2_0}\t{neg_E2_0_}\n")
                    E2_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                elif current_time - E3_time == 40 or E3_time == 30:
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E3 )
                  #  f.write(f"{current_time}\t{neg_E3_0}\t{neg_E3_0_}\n")
                    E3_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                # get the current simulation time
                time = traci.simulation.getTime()

            else:   
                # our main algorithm  
                for edge in edges:
                    waiting_time_edge = traci.edge.getWaitingTime(edge)
                    waiting_vehicles_number = traci.edge.getLastStepVehicleNumber(edge)
                    normalized_waiting_time = waiting_time_edge / Total_waiting_time
                    normalized_waiting_vehicles = waiting_vehicles_number/Total_vehicles
                    # give some mathematical function to the "traffic_value"
                    traffic_value = pow(normalized_waiting_time,(1-(i/(Total_i))))*pow(normalized_waiting_vehicles,i/(Total_i))
                    #traffic_value = normalized_waiting_time*normalized_waiting_vehicles
                    #print(normalized_waiting_time,normalized_waiting_vehicles)
                    if traffic_value > highest_traffic_value:
                        highest_traffic_value = traffic_value
                        most_conjested_edge = edge
                
                if  most_conjested_edge == "-E0":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E0 )
                   # f.write(f"{current_time}\t{neg_E0_0}\t{neg_E0_0_}\n")
                    E0_time = traci.simulation.getTime() # to get time when the traffic was green for this lane

                if most_conjested_edge == "-E1":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E1 )
                  #  f.write(f"{current_time}\t{neg_E1_0}\t{neg_E1_0_}\n")
                    E1_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                
                if most_conjested_edge == "-E2":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E2 )
                 #   f.write(f"{current_time}\t{neg_E2_0}\t{neg_E2_0_}\n")
                    E2_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                if most_conjested_edge == "-E3":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E3 )
                   # f.write(f"{current_time}\t{neg_E3_0}\t{neg_E3_0_}\n")
                    E3_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
       
                    
                #phase_duration = highest_traffic_value*T
                # print(phase_duration)

                # get the current simulation time
                time = traci.simulation.getTime()

            # advance the simulation
        traci.simulationStep()
        
    Average_Waiting_Time = cumulative_waiting_time/count

    #print(Average_Waiting_Time)
    traci.close()    
   # lane_waiting_values = [l1_cumulative_waiting_time,l2_cumulative_waiting_time,l3_cumulative_waiting_time,l4_cumulative_waiting_time,l5_cumulative_waiting_time,l6_cumulative_waiting_time,l7_cumulative_waiting_time,l8_cumulative_waiting_time, l9_cumulative_waiting_time,l10_cumulative_waiting_time,l11_cumulative_waiting_time,l12_cumulative_waiting_time]
    #max_lane1 = np.max(l1_cumulative_waiting_time,l2_cumulative_waiting_time,l3_cumulative_waiting_time,l4_cumulative_waiting_time,l5_cumulative_waiting_time)
    #max_lane2 = np.max(l6_cumulative_waiting_time,l7_cumulative_waiting_time,l8_cumulative_waiting_time, l9_cumulative_waiting_time,l10_cumulative_waiting_time,l11_cumulative_waiting_time,l12_cumulative_waiting_time)
    #max_lane = np.argmax(lane_waiting_values)
    #max_lane_value = np.amax(lane_waiting_values)
    #sum_lane = np.sum(lane_waiting_values)
    sys.stdout.flush()
   # print(max_lane,max_lane_value,sum_lane)
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
np.savetxt(f"SOTL CP Edge.csv",data)

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
plt.savefig('Waiting Time Vs Simulation Time SOTL CP Edge.png')

# Show the plot
plt.show()
    
     

    