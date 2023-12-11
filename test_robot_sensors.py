import math
import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
# if RemoteAPIClient import fails, install with : 
# python3 -m pip install coppeliasim-zmqremoteapi-client

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import cv2

def init_lidar(sim):
    lidar1_handle = sim.getObject("/robot/lidar/lidar1")
    lidar2_handle = sim.getObject("/robot/lidar/lidar2")
    lidar3_handle = sim.getObject("/robot/lidar/lidar3")
    handles = [lidar1_handle, lidar2_handle, lidar3_handle]
    resol_x = sim.getObjectInt32Param(handles[0],sim.visionintparam_resolution_x)
    resol_y = sim.getObjectInt32Param(handles[0],sim.visionintparam_resolution_y)
    resol = [resol_x, resol_y]
    angle_fov = np.degrees(sim.getObjectFloatParam(handles[0],sim.visionfloatparam_perspective_angle))
    print ("resol x",resol_x,"resol y",resol_y,"fov",angle_fov)
    ofs = angle_fov/resol_x/2 
    lidar_angles_1 = -angle_fov/2.0 + np.linspace(ofs,angle_fov-ofs,resol_x)
    lidar_angles_1[np.where(lidar_angles_1<0)] += 360.0
    lidar_angles_2 = angle_fov/2.0 + np.linspace(ofs,angle_fov-ofs,resol_x)
    lidar_angles_3 = angle_fov + angle_fov/2.0 + np.linspace(ofs,angle_fov-ofs,resol_x)
    lidar_angles = np.concatenate((lidar_angles_1,lidar_angles_2,lidar_angles_3))
    return handles,lidar_angles,resol

def get_lidar_scan(sim,handles,resol,simVision):
    ranges = []
    angles = []
    ang_ofs = [0.0,120.,240.]
    sector = [True,True,True] # for debug
    for ih in range(3):
        if sector[ih]:
            handle = handles[ih]
            simVision.sensorDepthMapToWorkImg(handle)
            points_ok = False
            try:
                trig,points_packed = simVision.coordinatesFromWorkImg(handle,[resol[0],resol[1]],False,False)
                points = sim.unpackFloatTable(points_packed,0,0,0)
                points_ok = True
            except:
                pass
            if points_ok:
                n_points = int(points[0]*points[1])
                #print (handle, n_points)
                for i in range(int(n_points)):
                    y = -points[2+i*4]
                    x = points[2+2+i*4]
                    dist = points[3+2+i*4]
                    ang0 = np.degrees(np.arctan2(y,x))
                    ang = ang0+ang_ofs[ih]
                    #print (x,y,dist,ang0,ang)
                    # 0 degree in forward direction, 90 degrees on the right  
                    ang = 90.0 + ang
                    ranges.append(dist)
                    angles.append(ang)
    return ranges,angles

def plot_lidar_scan (ranges,angles,fig,sc):
    x = ranges*np.cos(np.radians(angles))
    y = ranges*np.sin(np.radians(angles))
    sc.set_offsets(np.column_stack((x, y)))
    fig.canvas.draw_idle()
    plt.pause(0.01)

def get_video_camera_image (sim,front_camera_handle):
    options = 0
    rgba_cut_off = 0.0 # default
    pos = [0,0] # default
    size = [0,0] # default
    image_packed, resolution = sim.getVisionSensorImg(front_camera_handle, options, rgba_cut_off, pos, size)
    image = np.frombuffer(image_packed, dtype=np.uint8)
    image = np.reshape(image,(resolution[1],resolution[0],3))
    image_cv = image[...,[2,1,0]].copy()
    image_cv = cv2.flip(image_cv, 1)
    return image_cv,resolution

def display_video_camera_image (image_cv):
    cv2.imshow('front camera image', image_cv)
    cv2.waitKey(1)


client = RemoteAPIClient()
sim = client.require('sim')
simVision = client.require('simVision')
sim.setStepping(False)

left_motor_handle = sim.getObjectHandle("left_motor")
right_motor_handle = sim.getObjectHandle("right_motor")
front_camera_handle = sim.getObjectHandle("front_camera")

# init LIDAR
lidar_handles,lidar_angles,resol = init_lidar(sim)
# theoretical lidar_angles are just  for test

# init LIDAR plot
dmax = 1.8
fig, ax = plt.subplots(figsize=(5, 5))
sc = ax.scatter([], [], s=5, c='b', marker='o')
ax.set_title('2D LIDAR')
ax.set_xlabel('X (right)')
ax.set_ylabel('Y (forward)')
ax.set_xbound([-dmax,dmax])
ax.set_ybound([-dmax,dmax])
ax.axis('equal')
ax.grid(True)
plt.ion() 
plt.show()

# motion test
target_velocity = math.radians(30) # 30 degrees/s
motion_params = []
sim.setJointTargetVelocity(left_motor_handle, target_velocity , motion_params)
sim.setJointTargetVelocity(right_motor_handle, -target_velocity , motion_params)

duration = 60.0
dtloop = 0.1
t0 = time.time()
while True:
    if time.time()-t0>duration:
        break

    image_cv,resolution = get_video_camera_image (sim,front_camera_handle)
    display_video_camera_image (image_cv)

    depths_det,angles_det = get_lidar_scan(sim,lidar_handles,resol,simVision)
    plot_lidar_scan (depths_det,angles_det,fig,sc)

    time.sleep (dtloop)

target_velocity = 0
sim.setJointTargetVelocity(left_motor_handle, target_velocity , motion_params)
sim.setJointTargetVelocity(right_motor_handle, target_velocity , motion_params)

