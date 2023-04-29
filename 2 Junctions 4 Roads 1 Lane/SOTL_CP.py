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

def run_simulation(Total_i,i,j,simulation_duration):
    # main simulation loop
    # define the junction ID
    junction_id1 = "J2"
    junction_id2 = "J3"
    

    lane1 = ['E0_0','-E4_0','-E3_0','-E1_0'] #left lanes
    lane2 = ['E1_0','-E5_0','-E2_0','-E6_0'] #right lanes
    
    # define the duration of each phase
    phase_duration = 10
    lane_length = traci.lane.getLength('E1_0') #legth of the lane

    network_waiting_time_list = [] #list for storing waiting time per step of simulation
    while traci.simulation.getTime() < simulation_duration:
            # get the current simulation time
            current_time = traci.simulation.getTime() #simulation time at that point of simulation
            state = "GGGrrrrrrrrrrrrrrrrrrrrr" 
            total_waiting_time1 = 0 #total waiting time over all the edges in the left junction 
            total_waiting_time2 = 0  #total waiting time over all the edges in the right junction
            
            for lane in lane1:
                    waiting_time_lane1 = traci.lane.getWaitingTime(lane) # waiting time for the corresponding lane                   
                    total_waiting_time1 += waiting_time_lane1
                   
            for lane in lane2:                   
                    waiting_time_lane2 = traci.lane.getWaitingTime(lane)                  
                    total_waiting_time2 += waiting_time_lane2

            network_waiting_time = total_waiting_time1+total_waiting_time2 #total waiting time over the whole network
            network_waiting_time_list.append(network_waiting_time)

            # switch the traffic light state based on the current time
            if current_time % phase_duration == 0:
                max_waiting_lane1 = None #store the lane with max traffic value for left junction
                max_waiting_lane2 = None #store the lane with max traffic value for right junction
                total_waiting_time1 = 0
                total_waiting_time2 = 0                
                total_vehicles1 = 0 #total waiting time over all the edges in the left junction
                total_vehicles2 = 0 #total waiting time over all the edges in the right junction
                total_length_vehicle_E1 = 0 #total legth of the vehicles in the lane "E1_0"
                total_length_vehicle_neg_E1 = 0 #total legth of the vehicles in the lane "-E1_0"
                normalized_waiting_cars1 =  0
                normalized_waiting_cars2 =  0
                normalized_waiting_time1 = 0
                normalized_waiting_time2 = 0
                max_traffic_value1 = 0 #max traffic value in left junction
                max_traffic_value2 = 0 #max traffic value in right junction
                for lane in lane1:
                    waiting_cars1 = traci.lane.getLastStepVehicleNumber(lane) # number of vehicles for the corresponding lane 
                    waiting_time_lane1 = traci.lane.getWaitingTime(lane) # waiting time for the corresponding lane 
                    total_vehicles1 += waiting_cars1
                    total_waiting_time1 += waiting_time_lane1
                   
                for lane in lane2:
                    waiting_cars2 = traci.lane.getLastStepVehicleNumber(lane)
                    waiting_time_lane2 = traci.lane.getWaitingTime(lane)
                    total_vehicles2 += waiting_cars2
                    total_waiting_time2 += waiting_time_lane2
                
                #if there is no parameter to decide which lane to open, then just open any one, as in this case it opens North_edge_left_junction 
                if total_waiting_time1 == 0 or total_waiting_time2 == 0 or total_vehicles1 == 0 or total_vehicles2 == 0:
                  traci.trafficlight.setRedYellowGreenState(junction_id2, state ) 
                else:
                 for lane in lane1:
                    waiting_cars1 = traci.lane.getLastStepVehicleNumber(lane)
                    waiting_time_lane1 = traci.lane.getWaitingTime(lane)
                    normalized_waiting_cars1 = waiting_cars1/total_vehicles1
                    normalized_waiting_time1 = waiting_time_lane1/total_waiting_time1
                    traffic_value1 = pow(normalized_waiting_time1,(1-(i/(Total_i))))*pow(normalized_waiting_cars1,(i/(Total_i))) #traffic value, it will be used to determine the which edge to open
                    if traffic_value1 > max_traffic_value1:
                        max_traffic_value1 = traffic_value1
                        max_waiting_lane1 = lane

                 for lane in lane2:
                    waiting_cars2 = traci.lane.getLastStepVehicleNumber(lane)
                    waiting_time_lane2 = traci.lane.getWaitingTime(lane)
                    normalized_waiting_cars2 = waiting_cars2/total_vehicles2
                    normalized_waiting_time2 = waiting_time_lane2/total_waiting_time2
                    traffic_value2 = pow(normalized_waiting_time2,(1-(j/(Total_i))))*pow(normalized_waiting_cars2,(j/(Total_i)))
                    if traffic_value2 > max_traffic_value2:
                        max_traffic_value2 = traffic_value2
                        max_waiting_lane2 = lane
                 
                 #calculate the total lengths of vehicles in both the middle lanes 
                 vehicle_ids_E1 = traci.lane.getLastStepVehicleIDs('E1_0')
                 vehicle_ids_neg_E1 = traci.lane.getLastStepVehicleIDs('-E1_0')
                 for vehicle_id in vehicle_ids_E1:
                     length = traci.vehicle.getLength(vehicle_id)
                     total_length_vehicle_E1 += length
                 for vehicle_id in vehicle_ids_neg_E1:
                     length = traci.vehicle.getLength(vehicle_id)
                     total_length_vehicle_neg_E1 += length

                 
                 #open the lanes with max traffic value for each junction but open both the middle lanes if length of all the vehicles is greter than a certain threshold 
                 #open both the middle lanes if anyone of them is opened
                 for lane in lane1:
                  if max_waiting_lane1 == '-E1_0' or total_length_vehicle_E1 >  (lane_length -40) or total_length_vehicle_neg_E1 >   (lane_length-40):
                    state = "rrrGGGrrrrrrrrrrrrrrrGGG"   #open Middle edges                 
                  elif max_waiting_lane1 == 'E0_0':
                    state = "rrrrrrrrrGGGrrrrrrrrrrrr"  #open West_edges_left_junction
                  elif max_waiting_lane1 == '-E4_0':
                    state = "GGGrrrrrrrrrrrrrrrrrrrrr"  #open North_edge_left_junction
                  elif max_waiting_lane1 == '-E3_0':
                    state = "rrrrrrGGGrrrrrrrrrrrrrrr" #open South_edges_left_junction


                 for lane in lane2:
                  if max_waiting_lane2 == 'E1_0':
                    state = "rrrGGGrrrrrrrrrrrrrrrGGG"    #open Middle edges 
                                   
                  elif max_waiting_lane2 == '-E5_0':
                    state = state[0:12]+"GGG"+state[15:24] #open North_edges_right_junction
                    
                  elif max_waiting_lane2 == '-E2_0':
                    state = state[0:15]+"GGG"+state[18:24]  #open East_edges_right_junction
                    
                  elif max_waiting_lane2 == '-E6_0':
                    state = state[0:18]+"GGG"+state[21:24]  #open South_edges_right_junction  

                 for lane in lane1:
                    if max_waiting_lane1 == '-E1_0' or total_length_vehicle_E1 >  (lane_length -40) or total_length_vehicle_neg_E1 >   (lane_length-40):
                      state = "rrrGGGrrrrrrrrrrrrrrrGGG"  #open Middle edges 
                                   
                 traci.trafficlight.setRedYellowGreenState(junction_id2, state ) #change state of traffic light to "state"
                    
            traci.simulationStep() #go on to the next step

    traci.close()
    sys.stdout.flush()
    print("Length of middle lane",lane_length)
    average_waiting_time = np.average(network_waiting_time_list)
    print("Average Waiting Time",average_waiting_time)
    return network_waiting_time_list,average_waiting_time


if __name__ == "__main__":
    options = get_options()

    # check binary
    sumoBinary = checkBinary('sumo')    
    # traci starts sumo as a subprocess and then this script connects and runs
    config_file = os.path.join("E:\ME308 Project\Test8", "Configuration.sumocfg")
    traffic_scale = 0.6
    simulation_duration = 3100
    Total_i = 10
    data = np.zeros((simulation_duration, (Total_i+1)*(Total_i+1))) #empty array for storing the waiting time data
    avg = [] #empty array for storing the average waiting time data
    for i in range(Total_i+1):
      for j in range(Total_i+1):
        print(i,j,(i*(Total_i+1)+j)) #i,j corresponds to the weights of of the parameters in the traffic value
        sumo_cmd = [sumoBinary, "-c", config_file, "--no-warnings",f'--scale={traffic_scale}',"--start", "--quit-on-end"]
        traci.start(sumo_cmd) #start sumo
        n=run_simulation(Total_i,i,j,simulation_duration)
        m=n[0] #network's waiting time 
        data[:,(i*(Total_i+1)+j)]=m #store the waiting time data
        a=n[1]  #network's average waiting time 
        avg.append(a) #append average waiting time 
    pos = np.argmin(avg) #postion of run of the minimum average waiting time data
    avg_min = np.amin(avg) #minimum average waiting time
    min_i,min_j = int(pos/(Total_i+1)),int(pos%(Total_i+1))  #iteration numbers of minimum average waiting time data
    print(pos,min_i,min_j,avg_min)
    np.savetxt('CP_min.csv',data[:,(min_i*(Total_i+1)+min_j)]) #save the waiting time of the minimum average waiting time run
    np.savetxt('CP Average.csv',avg)  #save the average waiting times     



# Create a new figure and axis object
fig, ax = plt.subplots()

# Plot each column of data with a different color
for i in range((Total_i+1)*(Total_i+1)):
    ax.plot(data[:, i], label=f'Iteration {i+1}')

# Set the axis labels and title
ax.set_xlabel('Simulation Time')
ax.set_ylabel('Waiting Time')
ax.set_title('Waiting Time Vs Simulation Time')
# Add a legend
ax.legend()

# save the plot
plt.savefig('Waiting Time Vs Simulation Time SOTL CP.png')

# Show the plot
plt.show()


