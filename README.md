# Traffic-Light-Optimization

## Installation and Use Guide



1.Install SUMO in your system using the following [**link**](https://sumo.dlr.de/docs/Downloads.php) or you can type **SUMO Simulator** in your browser.

2.[Setup the environment variable](https://sumo.dlr.de/docs/Basics/Basic_Computer_Skills.html)

3.You can familiarize with SUMO by following the [**SUMO_Tutorial.txt**](https://github.com/21skar4/Traffic-Light-Optimization/blob/main/SUMO_Tutorial.txt) file in the Repository or you can directly run the python code files available in the folders in the Repository. 

Tutorials:
- https://sumo.dlr.de/docs/Tutorials/index.html
- https://www.youtube.com/watch?v=urKtJj87X5M

## Files and their Usage

1.**Network.net.xml :** This file is the network file, it is the file that defines the road network. You can build this file in **netedit** which is by default installed with **SUMO** but you have to make it SUMO-readable for which you can look up the **SUMO_Tutorial.txt** file.

2.**Routes.rou.xml :** This file contains the information regarding the routes taken by the vehilces in the network.

3.**trips.trips.xml :** This file contains information regarding when which vehicles will start their journey.

4.**randomTrips.py :** This file is by default avaiable in the**C:\Program Files (x86)\Eclipse\Sumo\tools** if you installed SUMO in **C:\Program Files (x86)**. This file helps in building random traffic flow in your network and create files **Routes.rou.xml** and  **trips.trips.xml**.

5.**SUMO Configuartion.sumocfg :** It calls the **Network.net.xml**,**Routes.rou.xml** and **trips.trips.xml** to run the simulation based on the set simulation steps.If you run the simulation directly by clicking the **SUMO Configuartion.sumocfg**, the traffic state will change based on the  default **tlLogic** in the **Network.net.xm**l file and if you run through the given python files (using TraCI library), the traffic state will changed based on your python file tlLogic.

6.**Convention.txt :** This file contains the convention of the Traffic light state. 

Information regarding the other files (python files) are available in the Report file.


## Demo

[SUMO Demo using TraCI](https://drive.google.com/drive/folders/1Flu5SJ3A4qXv-_u8BIM6spz9AYDj60Pj?usp=sharing)


## Authors

- [Bhaskar Pegu](https://github.com/21skar4)
- [Sashreek Paul](https://github.com/21skar4)
- [Shreejash](https://github.com/21skar4)
- [Akhilesh](https://github.com/21skar4)


## License

[GNU General Public License v3.0](https://github.com/21skar4/Traffic-Light-Optimization/blob/main/LICENSE)
