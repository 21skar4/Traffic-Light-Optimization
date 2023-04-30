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
    edges = traci.edge.getIDList() #get lane ids
 
    # define the state strings for the traffic lights
    #for edge "-E0"
    neg_E0 = "GGGGGrrrrrrrrrrrrrrr" #open North edge
    
    #for edge "-E1"
    neg_E1 = "rrrrrGGGGGrrrrrrrrrr" #open East edge
    
    #for edge "-E2"
    neg_E2 = "rrrrrrrrrrGGGGGrrrrr" #open South edge

    #for edge "-E3"
    neg_E3 = "rrrrrrrrrrrrrrrGGGGG" #open West edge
    
    # define the duration of each phase
    phase_duration = 10.0 
    #to get total waiting time
    cumulative_waiting_time = 0.0
    count = 0
    #to store waiting time data
    waiting_time_data = []
    
    E0_time = traci.simulation.getTime()
    E1_time = traci.simulation.getTime()
    E2_time = traci.simulation.getTime()
    E3_time = traci.simulation.getTime()

    # start the main loop
    while traci.simulation.getTime() < simulation_duration:  # end the iteration if simulation time is greater than equal to simulation duration 
        # get the current simulation time
        current_time = traci.simulation.getTime()
        
        Total_vehicles = 0 #total vehicles in the network at that time
        Total_waiting_time = 0.0 #total waiting time in the network
        for edge in edges:
          waiting_time_edge = traci.edge.getWaitingTime(edge) #waiting time in the corresponding edge
          waiting_vehicles_number = traci.edge.getLastStepVehicleNumber(edge) #number of vehicles in the corresponding edge
          Total_waiting_time = Total_waiting_time + waiting_time_edge
          Total_vehicles = Total_vehicles + waiting_vehicles_number
         
        waiting_time_data.append(Total_waiting_time)
    
        cumulative_waiting_time += Total_waiting_time
        count +=1
        # switch the traffic light state based on the current time
        if current_time % phase_duration==0:  #for constant phase

            # if total waiting time or total vehilce is zero then apply fixed time algorithm or randomly open
            if Total_waiting_time == 0 or Total_vehicles ==0:
                # Fixed Time algorithm 
                if current_time - E0_time == 40 or E0_time == 0:
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E0 )
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

            else:   
                # our main algorithm  

                most_conjested_edge = None
                highest_traffic_value = 0.0 # our decesion making parameter
                #normalized values 
                normalized_waiting_time = 0.0 
                normalized_waiting_vehicles = 0.0
                for edge in edges:
                    waiting_time_edge = traci.edge.getWaitingTime(edge)
                    waiting_vehicles_number = traci.edge.getLastStepVehicleNumber(edge)
                    normalized_waiting_time = waiting_time_edge / Total_waiting_time
                    normalized_waiting_vehicles = waiting_vehicles_number/Total_vehicles
                    traffic_value = pow(normalized_waiting_time,(1-(i/(Total_i))))*pow(normalized_waiting_vehicles,i/(Total_i))
                    #get highets traffic value and its corresponding edge
                    if traffic_value > highest_traffic_value:
                        highest_traffic_value = traffic_value
                        most_conjested_edge = edge
                
                if  most_conjested_edge == "-E0":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E0 )
                    E0_time = traci.simulation.getTime() # to get time when the traffic was green for this edge

                if most_conjested_edge == "-E1":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E1 )
                    E1_time = traci.simulation.getTime() # to get time when the traffic was green for this edge
                
                if most_conjested_edge == "-E2":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E2 )
                    E2_time = traci.simulation.getTime() # to get time when the traffic was green for this edge
                if most_conjested_edge == "-E3":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E3 )
                    E3_time = traci.simulation.getTime() # to get time when the traffic was green for this edge
       
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
    
     

    