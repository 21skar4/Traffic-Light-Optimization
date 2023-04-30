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
    #for lane "-E0_0"
    neg_E0_0 = "GGGGGrrrrrrrrrrrrrrr"
    neg_E0_0_ ="North_to_West_&_South" 
    
    #for lane "-E0_1"
    neg_E0_1 = "GGGGGrrrrrrrrrrrrrrr"
    neg_E0_1_ ="North_to_South"

    #for lane "-E0_2"
    neg_E0_2 = "GGGGGrrrrrrrrrrrrrrr"
    neg_E0_2_ = "North_to_South_&_East"
    
    #for lane "-E1_0"
    neg_E1_0 = "rrrrrGGGGGrrrrrrrrrr"
    neg_E1_0_ ="East_to_West_&_North" 
    
    #for lane "-E1_1"
    neg_E1_1 = "rrrrrGGGGGrrrrrrrrrr"
    neg_E1_1_ ="East_to_West"

    #for lane "-E1_2"
    neg_E1_2 = "rrrrrGGGGGrrrrrrrrrr"
    neg_E1_2_ = "East_to_South_&_West"
    
    #for lane "-E2_0"
    neg_E2_0 = "rrrrrrrrrrGGGGGrrrrr"
    neg_E2_0_ ="South_to_East_&_North" 
    
    #for lane "-E2_1"
    neg_E2_1 = "rrrrrrrrrrGGGGGrrrrr"
    neg_E2_1_ ="South_to_North"

    #for lane "-E2_2"
    neg_E2_2 = "rrrrrrrrrrGGGGGrrrrr"
    neg_E2_2_ = "South_to_North_&_West"

    #for lane "-E3_0"
    neg_E3_0 = "rrrrrrrrrrrrrrrGGGGG"
    neg_E3_0_ ="West_to_East_&_South" 
    
    #for lane "-E3_1"
    neg_E3_1 = "rrrrrrrrrrrrrrrGGGGG"
    neg_E3_1_ ="West_to_East"

    #for lane "-E3_2"
    neg_E3_2 = "rrrrrrrrrrrrrrrGGGGG"
    neg_E3_2_ = "West_to_East_&_North"
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

    prev_time = 0.0
    # start the main loop
    E0_0_time = traci.simulation.getTime()
    E1_0_time = traci.simulation.getTime()
    E2_0_time = traci.simulation.getTime()
    E3_0_time = traci.simulation.getTime()
    while traci.simulation.getTime() < simulation_duration:  # end the iteration if sim_time is greater than 200
        # get the current simulation time
        current_time = traci.simulation.getTime()
        
        Total_vehicles = 0
        Total_waiting_time = 0.0
        for lane in lanes:
                waiting_time = traci.lane.getWaitingTime(lane)
                
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
 


        for lane in lanes:
          waiting_time_lane = traci.lane.getWaitingTime(lane)
          waiting_vehicles_number = traci.lane.getLastStepVehicleNumber(lane)
          Total_waiting_time = Total_waiting_time +  waiting_time_lane
          Total_vehicles = Total_vehicles + waiting_vehicles_number
         
        waiting_time_data.append(Total_waiting_time)
    
        cumulative_waiting_time += Total_waiting_time
        count +=1
        l = 10
        # switch the traffic light state based on the current time
        if current_time - (time + phase_duration) > traci.simulation.getDeltaT():
        #if current_time % l==0:   
            most_conjested_lane = None
            highest_traffic_value = 0.0 # our decesion making parameter

            #normalized values 
            normalized_waiting_time = 0.0 
            normalized_waiting_vehicles = 0.0

            # if total waiting time or total vehilce is zero then apply fixed time algorithm
            if Total_waiting_time == 0 or Total_vehicles ==0:
                # Fixed Time algorithm 
            
                if current_time - E0_0_time == 40 or E0_0_time == 0:
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E0_0 )
                   # f.write(f"{current_time}\t{neg_E0_0}\t{neg_E0_0_}\n")
                    E0_0_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                elif current_time - E1_0_time == 40 or E1_0_time == 10:
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E1_0 )
                   # f.write(f"{current_time}\t{neg_E1_0}\t{neg_E1_0_}\n")
                    E1_0_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                elif current_time - E2_0_time == 40 or E2_0_time== 20:
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E2_0 )
                   # f.write(f"{current_time}\t{neg_E2_0}\t{neg_E2_0_}\n")
                    E2_0_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                elif current_time - E3_0_time == 40 or E3_0_time == 30:
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E3_0 )
                  #  f.write(f"{current_time}\t{neg_E3_0}\t{neg_E3_0_}\n")
                    E3_0_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                # get the current simulation time
                
                
                
                phase_duration = 5.0
                # print(phase_duration)

                # get the current simulation time
                time = traci.simulation.getTime()

            else:   
                # our main algorithm  
                total_traffic_value = 0.0
                for lane in lanes:
                    waiting_time_lane = traci.lane.getWaitingTime(lane)
                    waiting_vehicles_number = traci.lane.getLastStepVehicleNumber(lane)
                    normalized_waiting_time = waiting_time_lane / Total_waiting_time
                    normalized_waiting_vehicles = waiting_vehicles_number/Total_vehicles
                    # give some mathematical function to the "traffic_value"
                    traffic_value = pow(normalized_waiting_time,(1-(i/(Total_i))))*pow(normalized_waiting_vehicles,i/(Total_i))
                    total_traffic_value+=traffic_value
                    #traffic_value = normalized_waiting_time*normalized_waiting_vehicles
                    #print(normalized_waiting_time,normalized_waiting_vehicles)
                    if traffic_value > highest_traffic_value:
                        highest_traffic_value = traffic_value
                        most_conjested_lane = lane 
                
                if  most_conjested_lane == "-E0_0":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E0_0 )
                   # f.write(f"{current_time}\t{neg_E0_0}\t{neg_E0_0_}\n")
                    E0_0_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                if  most_conjested_lane == "-E0_1":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E0_1 )
                  #  f.write(f"{current_time}\t{neg_E0_1}\t{neg_E0_1_}\n")
                    E0_1_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                if most_conjested_lane == "-E0_2":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E0_2 )
                  #  f.write(f"{current_time}\t{neg_E0_2}\t{neg_E0_2_}\n")
                    E0_2_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                if most_conjested_lane == "-E1_0":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E1_0 )
                  #  f.write(f"{current_time}\t{neg_E1_0}\t{neg_E1_0_}\n")
                    E1_0_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                if most_conjested_lane == "-E1_1":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E1_1 )
                  #  f.write(f"{current_time}\t{neg_E1_1}\t{neg_E1_1_}\n")
                    E1_1_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                if most_conjested_lane == "-E1_2":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E1_2 )
                   # f.write(f"{current_time}\t{neg_E1_2}\t{neg_E1_2_}\n")
                    E1_2_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                if most_conjested_lane == "-E2_0":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E2_0 )
                 #   f.write(f"{current_time}\t{neg_E2_0}\t{neg_E2_0_}\n")
                    E2_0_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                if most_conjested_lane == "-E2_1":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E2_1 )
                  #  f.write(f"{current_time}\t{neg_E2_1}\t{neg_E2_1_}\n")
                    E2_1_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                if most_conjested_lane == "-E2_2":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E2_2 )
                  #  f.write(f"{current_time}\t{neg_E2_2}\t{neg_E2_2_}\n")
                    E2_2_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                if most_conjested_lane == "-E3_0":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E3_0 )
                   # f.write(f"{current_time}\t{neg_E3_0}\t{neg_E3_0_}\n")
                    E3_0_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                if most_conjested_lane == "-E3_1":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E3_1 )
                    #f.write(f"{current_time}\t{neg_E3_1}\t{neg_E3_1_}\n")
                    E3_1_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                if most_conjested_lane == "-E3_2":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E3_2 )
                    #f.write(f"{current_time}\t{neg_E3_2}\t{neg_E3_2_}\n")
                    E3_2_time = traci.simulation.getTime() # to get time when the traffic was green for this lane
                    
                phase_duration = highest_traffic_value*T/total_traffic_value
                # print(phase_duration)

                # get the current simulation time
                time = traci.simulation.getTime()

            # advance the simulation
        traci.simulationStep()
        
    Average_Waiting_Time = cumulative_waiting_time/count

    #print(Average_Waiting_Time)
    traci.close()    
    lane_waiting_values = [l1_cumulative_waiting_time,l2_cumulative_waiting_time,l3_cumulative_waiting_time,l4_cumulative_waiting_time,l5_cumulative_waiting_time,l6_cumulative_waiting_time,l7_cumulative_waiting_time,l8_cumulative_waiting_time, l9_cumulative_waiting_time,l10_cumulative_waiting_time,l11_cumulative_waiting_time,l12_cumulative_waiting_time]
    #max_lane1 = np.max(l1_cumulative_waiting_time,l2_cumulative_waiting_time,l3_cumulative_waiting_time,l4_cumulative_waiting_time,l5_cumulative_waiting_time)
    #max_lane2 = np.max(l6_cumulative_waiting_time,l7_cumulative_waiting_time,l8_cumulative_waiting_time, l9_cumulative_waiting_time,l10_cumulative_waiting_time,l11_cumulative_waiting_time,l12_cumulative_waiting_time)
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