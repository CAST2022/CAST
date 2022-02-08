# CAST
## Executive Summary
Our covid sanitization robot will bridge the gap between the need for clean surfaces and the lack of workforce brought about by different circumstances. Our robot will utilize a gamepad controller to move and Lidar as an early warning system of moving obstacles. To sanitize surfaces, we have a robotic arm equipped with UV lights that kill bacteria upon exposure and three time of flight sensors that will take in proximity data and maintain a safe distance between the arm and the surface to be cleaned. 

To allow the user to test the effectiveness of the robot we are also creating a bacteria killed indicator. This indicator uses a UV sensor to measure the amount of UV C radiation absorbed by the area and has the capabilities to communicate using IOT. By incorporating this product, we are giving the user an ability to test the effectiveness of the robot, this will be useful for error detection. 

By incorporating lidar into our design we’re paving the way for the robot to be fully autonomous in the future, removing the need for the gamepad controller. With a fully autonomous robot the design will be able to clean a small area without human interaction.

## Directories
To view the Hardware CAD models, one must have a CAD modeling program that SUPPORTS .SLDPRT
The Software is split into two sections. The first section is the Robots Software, that is run on a Raspberry Pi. It uses Python coding to control the system. The second section is the UV Sensor, it uses an Ardiuno Nano and is controlled by C++ codes.

## Special Thanks
The team would like to start off by thanking everyone that has helped us get to this point in our project. Specifically, Dr. Biswas, David Malawey, Donald Bowen, Brey Carawey, Jorge Roa, Ricardo Castillo, Matthew Hammond, and Dr. Crosby. We’d also like to extend our thanks to the Texas A&M ETID department for the time and funding put into ensuring we have all the resources we need to complete this project.

## License
This work is licensed under the Creative Commons Attribution-ShareAlike 4.0 License. To view details visit [creativecommons.org](https://creativecommons.org/licenses/by-sa/4.0/legalcode)
