import os
import math
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
# if RemoteAPIClient import fails, install with : 
# python3 -m pip install coppeliasim-zmqremoteapi-client

client = RemoteAPIClient()
sim = client.require('sim')
sim.setStepping(False)

wheel_diameter = 0.05
wheel_thickness = 0.01
robot_base_length = 0.25
robot_base_width = 0.20
robot_base_height = 0.01
robot_top_height = 0.20

robot_all_handles = []
options = 0
robot_base_handle = sim.createPrimitiveShape(sim.primitiveshape_cuboid, 
                                        [robot_base_length, robot_base_width, robot_base_height], options)
sim.setObjectAlias(robot_base_handle, "robot base")
robot_base_z = robot_base_height/2.0+wheel_diameter/2.0
sim.setObjectPosition(robot_base_handle, [0,0,robot_base_z], sim.handle_world)

robot_top_handle = sim.createPrimitiveShape(sim.primitiveshape_cuboid, 
                                        [robot_base_length, robot_base_width, robot_base_height], options)
sim.setObjectAlias(robot_top_handle, "robot top")
robot_top_z = robot_base_z+robot_top_height-robot_base_height
sim.setObjectPosition(robot_top_handle, [0,0,robot_top_z], sim.handle_world)

pole_thickness = 0.01
dx2 = robot_base_length/2.0-pole_thickness/2.0
dy2 = robot_base_width/2.0-pole_thickness/2.0
vx = [-dx2,dx2,dx2,-dx2]
vy = [-dy2,-dy2,dy2,dy2]
robot_pole_z = robot_base_z-robot_base_height/2.0+robot_top_height/2.0
n_poles = 4
for i in range(n_poles):
    handle = sim.createPrimitiveShape(sim.primitiveshape_cuboid, 
                                        [pole_thickness, pole_thickness, robot_top_height], options)
    sim.setObjectPosition(handle, [vx[i],vy[i],robot_pole_z], sim.handle_world)
    robot_all_handles.append(handle)

robot_all_handles.append(robot_top_handle)
robot_all_handles.append(robot_base_handle)
for handle in robot_all_handles:
    sim.setObjectColor(handle, 0, sim.colorcomponent_ambient_diffuse, [0.0, 0.6, 0.8])
    sim.setObjectColor(handle, 0, sim.colorcomponent_specular, [0.9, 0.9, 0.9])
robot_handle = sim.groupShapes(robot_all_handles,False)
sim.setObjectAlias(robot_handle, "robot")

left_wheel_handle = sim.createPrimitiveShape(sim.primitiveshape_cylinder, 
                                             [wheel_diameter, wheel_diameter, wheel_thickness], options)
sim.setObjectAlias(left_wheel_handle, "left_wheel")
sim.setObjectOrientation(left_wheel_handle,[-math.pi/2.0,0,0],left_wheel_handle)
sim.setObjectPosition(left_wheel_handle, [0,(robot_base_width/2.0+wheel_thickness),wheel_diameter/2.0], sim.handle_world)
sim.setObjectColor(left_wheel_handle, 0, sim.colorcomponent_ambient_diffuse, [0.1, 0.1, 0.1])
sim.setObjectColor(left_wheel_handle, 0, sim.colorcomponent_specular, [0.9, 0.9, 0.9])

right_wheel_handle = sim.createPrimitiveShape(sim.primitiveshape_cylinder, 
                                             [wheel_diameter, wheel_diameter, wheel_thickness], options)
sim.setObjectAlias(right_wheel_handle, "right_wheel")
sim.setObjectOrientation(right_wheel_handle,[-math.pi/2.0,0,0],right_wheel_handle)
sim.setObjectPosition(right_wheel_handle, [0,-(robot_base_width/2.0+wheel_thickness),wheel_diameter/2.0], sim.handle_world)
sim.setObjectColor(right_wheel_handle, 0, sim.colorcomponent_ambient_diffuse, [0.1, 0.1, 0.1])
sim.setObjectColor(right_wheel_handle, 0, sim.colorcomponent_specular, [0.9, 0.9, 0.9])

options = 0
sizes = [0.05,0.01]
left_motor_handle = sim.createJoint(sim.joint_revolute_subtype, sim.jointmode_dynamic, options, sizes)
sim.setObjectAlias(left_motor_handle, "left_motor")
sim.setObjectOrientation(left_motor_handle,[-math.pi/2.0,0,0],left_motor_handle)
sim.setObjectPosition(left_motor_handle, [0,(robot_base_width/2.0-wheel_thickness),wheel_diameter/2.0], sim.handle_world)

right_motor_handle = sim.createJoint(sim.joint_revolute_subtype, sim.jointmode_dynamic, options, sizes)
sim.setObjectAlias(right_motor_handle, "right_motor")
sim.setObjectOrientation(right_motor_handle,[-math.pi/2.0,0,0],right_motor_handle)
sim.setObjectPosition(right_motor_handle, [0,-(robot_base_width/2.0+wheel_thickness),wheel_diameter/2.0], sim.handle_world)

# control motors with angular velocity 
sim.setObjectInt32Param(left_motor_handle,sim.jointintparam_dynctrlmode,sim.jointdynctrl_velocity)
sim.setObjectInt32Param(right_motor_handle,sim.jointintparam_dynctrlmode,sim.jointdynctrl_velocity)
# default 90 degrees/s , set to 0
target_velocity = 0 # rad/s
motion_params = []
sim.setJointTargetVelocity(left_motor_handle, target_velocity , motion_params)
sim.setJointTargetVelocity(right_motor_handle, -target_velocity , motion_params)

options = 0
front_caster_wheel_handle = sim.createPrimitiveShape(sim.primitiveshape_spheroid, [0.02, 0.02, 0.02], options)
sim.setObjectAlias(front_caster_wheel_handle, "front_caster_wheel")
sim.setObjectPosition(front_caster_wheel_handle, [robot_base_length/3.0,0,0.01], sim.handle_world)
options = 1 # force sensor
int_params = [0,3,2,0,0]
float_params = [0.01,1000.0,0,0,0]
front_caster_fixing_handle = sim.createForceSensor(options, int_params, float_params)
sim.setObjectAlias(front_caster_fixing_handle, "front_caster_fixing")
sim.setObjectPosition(front_caster_fixing_handle, [robot_base_length/3.0,0,wheel_diameter/2.0], sim.handle_world)
sim.setObjectColor(front_caster_wheel_handle, 0, sim.colorcomponent_ambient_diffuse, [0.1, 0.1, 0.1])
sim.setObjectColor(front_caster_wheel_handle, 0, sim.colorcomponent_specular, [0.9, 0.9, 0.9])

options = 0
rear_caster_wheel_handle = sim.createPrimitiveShape(sim.primitiveshape_spheroid, [0.02, 0.02, 0.02], options)
sim.setObjectAlias(rear_caster_wheel_handle, "rear_caster_wheel")
sim.setObjectPosition(rear_caster_wheel_handle, [-robot_base_length/3.0,0,0.01], sim.handle_world)
options = 1 # force sensor
int_params = [0,3,2,0,0]
float_params = [0.01,1000.0,0,0,0]
rear_caster_fixing_handle = sim.createForceSensor(options, int_params, float_params)
sim.setObjectAlias(rear_caster_fixing_handle, "rear_caster_fixing")
sim.setObjectPosition(rear_caster_fixing_handle, [-robot_base_length/3.0,0,wheel_diameter/2.0], sim.handle_world)
sim.setObjectColor(rear_caster_wheel_handle, 0, sim.colorcomponent_ambient_diffuse, [0.1, 0.1, 0.1])
sim.setObjectColor(rear_caster_wheel_handle, 0, sim.colorcomponent_specular, [0.9, 0.9, 0.9])

#assembles the robot's parts
keep_in_place = True
sim.setObjectParent(left_wheel_handle, left_motor_handle,keep_in_place)
sim.setObjectParent(left_motor_handle, robot_handle, keep_in_place)
sim.setObjectParent(right_wheel_handle, right_motor_handle,keep_in_place)
sim.setObjectParent(right_motor_handle, robot_handle, keep_in_place)
sim.setObjectParent(front_caster_wheel_handle, front_caster_fixing_handle, keep_in_place)
sim.setObjectParent(front_caster_fixing_handle, robot_handle, keep_in_place)
sim.setObjectParent(rear_caster_wheel_handle, rear_caster_fixing_handle, keep_in_place)
sim.setObjectParent(rear_caster_fixing_handle, robot_handle, keep_in_place)

# set the properties
prop = sim.objectspecialproperty_collidable or sim.objectspecialproperty_measurable or sim.objectspecialproperty_detectable
sim.setObjectSpecialProperty(robot_handle, prop)
sim.setObjectSpecialProperty(left_wheel_handle, prop)
sim.setObjectSpecialProperty(right_wheel_handle, prop)
sim.setObjectSpecialProperty(front_caster_wheel_handle, prop)
sim.setObjectSpecialProperty(rear_caster_wheel_handle, prop)

sim.setObjectInt32Param(robot_handle,sim.shapeintparam_respondable,1)
sim.setObjectInt32Param(robot_handle,sim.shapeintparam_static,0)
sim.setObjectInt32Param(left_wheel_handle,sim.shapeintparam_respondable,1)
sim.setObjectInt32Param(left_wheel_handle,sim.shapeintparam_static,0)
sim.setObjectInt32Param(right_wheel_handle,sim.shapeintparam_respondable,1)
sim.setObjectInt32Param(right_wheel_handle,sim.shapeintparam_static,0)
sim.setObjectInt32Param(front_caster_wheel_handle,sim.shapeintparam_respondable,1)
sim.setObjectInt32Param(front_caster_wheel_handle,sim.shapeintparam_static,0)
sim.setObjectInt32Param(rear_caster_wheel_handle,sim.shapeintparam_respondable,1)
sim.setObjectInt32Param(rear_caster_wheel_handle,sim.shapeintparam_static,0)

# add sensors

# 1) video camera 
options = 2
int_params = [800,600,0,0] # super VGA resolution 800x600 pixels
near_plane = 0.01
far_plane = 4.0
view_angle = math.radians(60.0)
sensor_size = 0.02
float_params = [near_plane, far_plane, view_angle, sensor_size, 0, 0, 0, 20, 40, 0, 0]
front_camera_handle = sim.createVisionSensor(options, int_params, float_params)
sim.setObjectAlias(front_camera_handle, "front_camera")
sim.setObjectOrientation(front_camera_handle,[0.0,math.radians(90.0),0.0],front_camera_handle)
sim.setObjectOrientation(front_camera_handle,[0.0,0.0,-math.radians(90.0)],front_camera_handle)
camera_height = robot_top_z + sensor_size
sim.setObjectPosition(front_camera_handle, [robot_base_length*0.52,0,camera_height], sim.handle_world)
# make camera look downwards, for example 15 degrees down
tilt_angle = -15.0
sim.setObjectOrientation(front_camera_handle,[math.radians(tilt_angle),0,0],front_camera_handle)
# add camera to robot
sim.setObjectParent(front_camera_handle, robot_handle, keep_in_place)

# 2) LIDAR
# full 360 degrees LIDAR can be simulated with 3 depth vision sensors with a FOV of 120 degrees
# the image has 256 pixels for 120 degrees , resolution around 1/2 degree
lidar_height = robot_base_z + robot_base_height/2.0 + 0.02
options = 2+4
nbeams = 256
int_params = [nbeams,1,0,0] # 2D Lidar (1D image, 1 pixel height)
near_plane = 0.01
far_plane = 4.0
view_angle = math.radians(120.0)
sensor_size = 0.01
float_params = [near_plane, far_plane, view_angle, sensor_size, 0, 0, 0, 20, 40, 0, 0]
lidar1_handle = sim.createVisionSensor(options, int_params, float_params)
sim.setObjectAlias(lidar1_handle, "lidar1")
# sim.setObjectInt32Param(lidar1_handle, sim.visionintparam_rgbignored, 1)
# sim.setObjectInt32Param(lidar1_handle, sim.visionintparam_depthignored, 0)
sim.setObjectInt32Param(lidar1_handle, sim.visionintparam_perspective_operation, 1) 
sim.setObjectOrientation(lidar1_handle,[0.0,math.radians(90.0),0.0],lidar1_handle)
sim.setObjectOrientation(lidar1_handle,[0.0,0.0,-math.radians(90.0)],lidar1_handle)
dx = 0.02
dy = 0.0
sim.setObjectPosition(lidar1_handle, [robot_base_length*0.4+dx,dy,lidar_height], sim.handle_world)

lidar2_handle = sim.createVisionSensor(options, int_params, float_params)
sim.setObjectAlias(lidar2_handle, "lidar2")
sim.setObjectInt32Param(lidar2_handle, sim.visionintparam_rgbignored, 1)
sim.setObjectInt32Param(lidar2_handle, sim.visionintparam_depthignored, 0)
sim.setObjectOrientation(lidar2_handle,[0.0,math.radians(90.0),0.0],lidar2_handle)
sim.setObjectOrientation(lidar2_handle,[0.0,0.0,-math.radians(90.0)],lidar2_handle)
pan_angle = -120.0
dx = 0.02*math.cos(math.radians(-pan_angle))
dy = 0.02*math.sin(math.radians(-pan_angle))
sim.setObjectPosition(lidar2_handle, [robot_base_length*0.4+dx,dy,lidar_height], sim.handle_world)
sim.setObjectOrientation(lidar2_handle,[0,math.radians(pan_angle),0],lidar2_handle)

lidar3_handle = sim.createVisionSensor(options, int_params, float_params)
sim.setObjectAlias(lidar3_handle, "lidar3")
sim.setObjectInt32Param(lidar3_handle, sim.visionintparam_rgbignored, 1)
sim.setObjectInt32Param(lidar3_handle, sim.visionintparam_depthignored, 0)
sim.setObjectOrientation(lidar3_handle,[0.0,math.radians(90.0),0.0],lidar3_handle)
sim.setObjectOrientation(lidar3_handle,[0.0,0.0,-math.radians(90.0)],lidar3_handle)
pan_angle = 120.0
dx = 0.02*math.cos(math.radians(-pan_angle))
dy = 0.02*math.sin(math.radians(-pan_angle))
sim.setObjectPosition(lidar3_handle, [robot_base_length*0.4+dx,dy,lidar_height], sim.handle_world)
sim.setObjectOrientation(lidar3_handle,[0,math.radians(pan_angle),0],lidar3_handle)

options = 0
lidar_handle = sim.createPrimitiveShape(sim.primitiveshape_cylinder, 
                                             [0.04,0.04,0.03], options)
sim.setObjectAlias(lidar_handle, "lidar")
sim.setObjectPosition(lidar_handle, [robot_base_length*0.4,0,lidar_height], sim.handle_world)
# build lidar and add it to robot
sim.setObjectParent(lidar1_handle, lidar_handle, keep_in_place)
sim.setObjectParent(lidar2_handle, lidar_handle, keep_in_place)
sim.setObjectParent(lidar3_handle, lidar_handle, keep_in_place)
sim.setObjectParent(lidar_handle, robot_handle, keep_in_place)
sim.setObjectColor(lidar_handle, 0, sim.colorcomponent_ambient_diffuse, [0.1, 0.1, 0.1])
sim.setObjectColor(lidar_handle, 0, sim.colorcomponent_specular, [0.1, 0.1, 0.1])

