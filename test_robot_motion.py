import math
import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
# if RemoteAPIClient import fails, install with : 
# python3 -m pip install coppeliasim-zmqremoteapi-client

client = RemoteAPIClient()
sim = client.require('sim')
sim.setStepping(False)

left_motor_handle = sim.getObjectHandle("left_motor")
right_motor_handle = sim.getObjectHandle("right_motor")

for i in range(2):
    # motion test linear
    target_velocity = math.radians(180) # 180 degrees/s
    motion_params = []
    sim.setJointTargetVelocity(left_motor_handle, target_velocity , motion_params)
    sim.setJointTargetVelocity(right_motor_handle, target_velocity , motion_params)
    duration = 10.0
    dtloop = 0.1
    t0 = time.time()
    while True:
        if time.time()-t0>duration:
            break
        time.sleep (dtloop)

    # motion test inplace turn
    target_velocity = math.radians(90) # 90 degrees/s
    motion_params = []
    sim.setJointTargetVelocity(left_motor_handle, target_velocity , motion_params)
    sim.setJointTargetVelocity(right_motor_handle, -target_velocity , motion_params)
    duration = 7.0
    dtloop = 0.1
    t0 = time.time()
    while True:
        if time.time()-t0>duration:
            break
        time.sleep (dtloop)

# stop
target_velocity = 0
sim.setJointTargetVelocity(left_motor_handle, target_velocity , motion_params)
sim.setJointTargetVelocity(right_motor_handle, target_velocity , motion_params)

