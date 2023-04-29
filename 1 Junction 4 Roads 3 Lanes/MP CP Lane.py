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
    phase_duration = 10

    # define output file 
    output_file1 = "MAX_PRE_TLState_Over_Time.txt"
    output_file2 = "MAX_PRE_Waiting_Time_Over_Time.txt"
    output_file3 = "MAX_PRE_Total_Waiting_Time_Over_Time.txt"
    output_file4 = "MAX_PRE_Number_of_Vehicles_Over_Time.txt"
    output_file5 = "MAX_PRE_Total_Number_of_Vehilces_Time_Over_Time_5c.txt"
   
    output_path1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_file1)
    output_path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_file2)
    output_path3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_file3)
    output_path4 = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_file4)
    output_path5 = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_file5)
    # start the main loop
    with open(output_path5, "w") as f5:
     with open(output_path3, "w") as f3:
      with open(output_path4, "w") as f4:
       with open(output_path2, "w") as f2:
        with open(output_path1, "w") as f1:
       # write the column header
         
         f5.write("Time\tTotal Number of Vehicles\n")
         f5.write("Time\tLane\tNumber of Vehicles\n")
         f3.write("Time\tTotal Waiting Time\n")
         f2.write("Time\tLane\tWaiting Time\n")
         f1.write("Time       \tState             \tMoving Direction      \tGreen Lane\n")
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
         while traci.simulation.getTime() < simulation_duration:
            
            # get the current simulation time
            current_time = traci.simulation.getTime()
                        #write the waiting time entries over time 
            total_waiting_time = 0
            for lane in lanes:
                waiting_time = traci.lane.getWaitingTime(lane)
                total_waiting_time = total_waiting_time + waiting_time
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
                if max_waiting_lane == "-E0_0":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E0_0 )
                    f1.write(f"{current_time}\t{neg_E0_0}\t{neg_E0_0_}\t{max_waiting_lane}\n")
                
                if max_waiting_lane == "-E0_1":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E0_1 )
                    f1.write(f"{current_time}\t{neg_E0_1}\t{neg_E0_1_}\t{max_waiting_lane}\n")
                
                if max_waiting_lane == "-E0_2":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E0_2 )
                    f1.write(f"{current_time}\t{neg_E0_2}\t{neg_E0_2_}\t{max_waiting_lane}\n")
                
                if max_waiting_lane == "-E1_0":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E1_0 )
                    f1.write(f"{current_time}\t{neg_E1_0}\t{neg_E1_0_}\t{max_waiting_lane}\n")
               
                if max_waiting_lane == "-E1_1":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E1_1 )
                    f1.write(f"{current_time}\t{neg_E1_1}\t{neg_E1_1_}\t{max_waiting_lane}\n")
                
                if max_waiting_lane == "-E1_2":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E1_2 )
                    f1.write(f"{current_time}\t{neg_E1_2}\t{neg_E1_2_}\t{max_waiting_lane}\n")
               
                if max_waiting_lane == "-E2_0":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E2_0 )
                    f1.write(f"{current_time}\t{neg_E2_0}\t{neg_E2_0_}\t{max_waiting_lane}\n")
                
                if max_waiting_lane == "-E2_1":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E2_1 )
                    f1.write(f"{current_time}\t{neg_E2_1}\t{neg_E2_1_}\t{max_waiting_lane}\n")

                if max_waiting_lane == "-E2_2":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E2_2 )
                    f1.write(f"{current_time}\t{neg_E2_2}\t{neg_E2_2_}\t{max_waiting_lane}\n")
                
                if max_waiting_lane == "-E3_0":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E3_0 )
                    f1.write(f"{current_time}\t{neg_E3_0}\t{neg_E3_0_}\t{max_waiting_lane}\n")
               
                if max_waiting_lane == "-E3_1":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E3_1 )
                    f1.write(f"{current_time}\t{neg_E3_1}\t{neg_E3_1_}\t{max_waiting_lane}\n")
                
                if max_waiting_lane == "-E3_2":
                    traci.trafficlight.setRedYellowGreenState(junction_id, neg_E3_2 )
                    f1.write(f"{current_time}\t{neg_E3_2}\t{neg_E3_2_}\t{max_waiting_lane}\n")




            

            #write the number of vehicles entries over time 
            total_number_vehicles = 0
            for lane in lanes:
                number_of_vehicles = traci.lane.getWaitingTime(lane)
                total_number_vehicles = total_number_vehicles + number_of_vehicles         

            # advance the simulation
            traci.simulationStep()

        traci.close()
        lane_waiting_values = [l1_cumulative_waiting_time,l2_cumulative_waiting_time,l3_cumulative_waiting_time,l4_cumulative_waiting_time,l5_cumulative_waiting_time,l6_cumulative_waiting_time,l7_cumulative_waiting_time,l8_cumulative_waiting_time, l9_cumulative_waiting_time,l10_cumulative_waiting_time,l11_cumulative_waiting_time,l12_cumulative_waiting_time]
        #max_lane1 = np.max(l1_cumulative_waiting_time,l2_cumulative_waiting_time,l3_cumulative_waiting_time,l4_cumulative_waiting_time,l5_cumulative_waiting_time)
        #max_lane2 = np.max(l6_cumulative_waiting_time,l7_cumulative_waiting_time,l8_cumulative_waiting_time, l9_cumulative_waiting_time,l10_cumulative_waiting_time,l11_cumulative_waiting_time,l12_cumulative_waiting_time)
        max_lane = np.argmax(lane_waiting_values)
        max_lane_value = np.amax(lane_waiting_values)
        sum_lane = np.sum(lane_waiting_values)
        sys.stdout.flush()
        print(max_lane,max_lane_value,sum_lane)
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
    simulation_duration = 1000
    traffic_scale = 0.6
    config_file = os.path.join("E:\ME308 Project\Test7", "SUMO Configuration.sumocfg")
    sumo_cmd = [sumoBinary, "-c", config_file,f'--scale={traffic_scale}']
    traci.start(sumo_cmd)
    m=run(simulation_duration)
    print(np.average(m))
    np.savetxt("MP CP Lane.csv",m)


# Create a new figure and axis object
fig, ax = plt.subplots()

# Plot each column of data with a different color

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