# CoppeliaSim - Coupe de France de Robotique 2024

Use 'Coupe de France Robotique 2024' challenge as a tutorial for the use of CoppeliaSim EDU ZeroMQ remote library

## Tutorial

See draft version of the tutorial [here](./docs/tutorial_2023.pdf)

## Requirements

Make sure to have the following Python modules installed :
 * pyzmq
 * coppeliasim-zmqremoteapi-client

This can be done by opening a terminal and executing in the command line :
 ```bash
python3 -m pip install pyzmq coppeliasim-zmqremoteapi-client
 ```

## Creating and testing the scene

### Creation

Start CoppeliaSim, an empty scene should appear.

The creation of the scene is achieved with 4 Python programs :
 * create_arena.py
 * add_pots.py
 * add_plants.py
 * create_robot.py

This can be done by opening a terminal and executing Python in the command line :
```bash
python3 create_arena.py
python3 add_pots.py
python3 add_plants.py
python3 create_robot.py
```


### Test

Start simulation by clicking on the start simulation button on CoppeliaSim.

The execute the followings commands :
```bash
python3 test_robot_motion.py
python3 test_robot_sensors.py
```

### Issues

* add external parts of the arena
* explain how to add video camera and LIDAR sensors in the tutorial
 

