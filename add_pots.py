import os
import math
import numpy as np
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
# if RemoteAPIClient import fails, install with : 
# python3 -m pip install coppeliasim-zmqremoteapi-client

client = RemoteAPIClient()
sim = client.require('sim')
sim.setStepping(False)

dir_path_stl = os.path.join(os.getcwd(),"3D_FINALE_V1/stl/")
file_format = 0 # auto detect format
file_name = os.path.join(dir_path_stl,'pot_MR.stl')
options = 16 # tries to preserve textures
identical_vertice_tolerance = 0.0 # default
scaling_factor = 0.001 # mm to m
pot_handle = sim.importShape(file_format, file_name, options, 
                               identical_vertice_tolerance, scaling_factor)
sim.setObjectAlias(pot_handle, "pot")
sim.setObjectColor(pot_handle, 0, sim.colorcomponent_ambient_diffuse, [0.5, 0.5, 0.5])
sim.setObjectColor(pot_handle, 0, sim.colorcomponent_specular, [0.9, 0.9, 0.9])

# create a faster dynamic shape
# from create_simple_dynamic_shapes.py
# pot dynamic shape is a base cylinder with poles
pole_diameter = 0.008
base_diameter = 0.063-2*pole_diameter
top_diameter = 0.070-2*pole_diameter
base_height = 0.005
pole_height = 0.064
pot_all_handles = []
options = 0
pot_base_handle = sim.createPrimitiveShape(sim.primitiveshape_cylinder, 
                                        [base_diameter,base_diameter,base_height], options)
sim.setObjectPosition (pot_base_handle, [0,0,base_height/2], pot_base_handle)
# add cuboid poles
n_poles = 18
for i in range(n_poles):
    ang = math.radians(i*360.0/n_poles)
    r = (base_diameter+top_diameter)/4.0+pole_diameter/2.0    
    x = r*math.cos(ang)
    y = r*math.sin(ang)
    handle = sim.createPrimitiveShape(sim.primitiveshape_cuboid, 
                                        [pole_diameter/5.0,pole_diameter,pole_height], options)
    sim.setObjectOrientation(handle, [0.0, 0.0, ang], handle)
    ang_cone = math.atan2(top_diameter-base_diameter,pole_height) # approx
    sim.setObjectOrientation(handle, [0.0, ang_cone, 0.0], handle)
    sim.setObjectPosition (handle, [x,y,0.002+pole_height/2], -1)
    pot_all_handles.append(handle)

# add bottom contacts (half spheres)
n_contacts = 3
for i in range(n_contacts):
    ang = math.radians(i*360.0/n_contacts)
    r = 0.4*base_diameter
    contact_diameter = 0.002
    x = r*math.cos(ang)
    y = r*math.sin(ang)    
    handle = sim.createPrimitiveShape(sim.primitiveshape_spheroid, 
                                        [contact_diameter, contact_diameter, contact_diameter], options)
    sim.setObjectPosition (handle, [x,y,0.0], -1)
    pot_all_handles.append(handle)

# the axis frame of grouped objects seems to be the frame of the last object
# so we place the base at the end    
pot_all_handles.append(pot_base_handle) 

for handle in pot_all_handles:
    prop = sim.objectspecialproperty_collidable 
    prop += sim.objectspecialproperty_measurable
    prop += sim.objectspecialproperty_detectable
    sim.setObjectInt32Param(handle,sim.shapeintparam_respondable,1) # respondable
    sim.setObjectInt32Param(handle,sim.shapeintparam_static,0) # dynamic
    sim.setObjectInt32Param(handle,sim.objintparam_visibility_layer,0) # non visible
    sim.setObjectSpecialProperty(handle, prop) # usable by all sensors
    mass0 = sim.getShapeMass(handle)
    if handle == pot_base_handle:
        mass = mass0 * 5.0
    else: 
        mass = mass0 / 5.0
    sim.setShapeMass(handle,mass)
    #print ("mass",mass0,mass)

pot_dyn_handle = sim.groupShapes(pot_all_handles,False)
sim.setObjectAlias(pot_dyn_handle, "pot_dyn")

# save the dynamic object for tutorial
vertices, indices, normals = sim.getShapeMesh(pot_dyn_handle)
file_name = os.path.join(dir_path_stl,'pot_dyn_final_way_mesh.stl')
options = 0
format_type = 4 # STL binary
scaling_factor = 1000 # to mm
sim.exportMesh(format_type,file_name,options,scaling_factor,[vertices],[indices])


def add_pot (pot_num,xc,yc,zc,dx,dy,dz,pot_handle,pot_dyn_handle):
    for i in range(6):
        x = xc + dx[i]
        y = yc + dy[i]
        z = zc + dz[i] + 0.00
        pot_num+=1
        copy_handles = sim.copyPasteObjects([pot_handle, pot_dyn_handle], 0)
        keep_in_place = True
        sim.setObjectParent(copy_handles[0],copy_handles[1],keep_in_place)
        sim.setObjectPosition (copy_handles[1], [x,y,z], copy_handles[0])
        object_name = "pot dyn %2.2d"%(pot_num)
        sim.setObjectAlias(copy_handles[1], object_name)
        object_name = "pot %2.2d"%(pot_num)
        sim.setObjectAlias(copy_handles[0], object_name)
    return pot_num

xc = -1.435
yc = 0.375
bounding_box = sim.getShapeBB(pot_dyn_handle)
zc = bounding_box[2]/2.0
zc = 0.01
dx = [0.0,0.0,0.0,0.0,0.07,0.07]
dy = [-0.08,0.0,0.0,0.08,-0.04,0.04]
dz = [0.0,0.0,0.037,0.0,0.0,0.0]
pot_num = 0
pot_num = add_pot (pot_num,xc,yc,zc,dx,dy,dz,pot_handle,pot_dyn_handle)

xc = -1.435
yc = -0.375
dx = [0.0,0.0,0.0,0.0,0.07,0.07]
dy = [-0.08,0.0,0.0,0.08,-0.04,0.04]
dz = [0.0,0.0,0.037,0.0,0.0,0.0]
pot_num = 0
pot_num = add_pot (pot_num,xc,yc,zc,dx,dy,dz,pot_handle,pot_dyn_handle)

xc = 1.435
yc = 0.375
dx = [0.0,0.0,0.0,0.0,-0.07,-0.07]
dy = [-0.08,0.0,0.0,0.08,-0.04,0.04]
dz = [0.0,0.0,0.037,0.0,0.0,0.0]
pot_num = add_pot (pot_num,xc,yc,zc,dx,dy,dz,pot_handle,pot_dyn_handle)

xc = 1.435
yc = -0.375
dx = [0.0,0.0,0.0,0.0,-0.07,-0.07]
dy = [-0.08,0.0,0.0,0.08,-0.04,0.04]
dz = [0.0,0.0,0.037,0.0,0.0,0.0]
pot_num = add_pot (pot_num,xc,yc,zc,dx,dy,dz,pot_handle,pot_dyn_handle)

xc = -0.5
yc = 0.965
dx = [-0.08,0.0,0.0,0.08,-0.04,0.04]
dy = [0.0,0.0,0.0,0.0,-0.07,-0.07]
dz = [0.0,0.0,0.037,0.0,0.0,0.0]
pot_num = add_pot (pot_num,xc,yc,zc,dx,dy,dz,pot_handle,pot_dyn_handle)

xc = 0.5
yc = 0.965
dx = [-0.08,0.0,0.0,0.08,-0.04,0.04]
dy = [0.0,0.0,0.0,0.0,-0.07,-0.07]
dz = [0.0,0.0,0.037,0.0,0.0,0.0]
pot_num = add_pot (pot_num,xc,yc,zc,dx,dy,dz,pot_handle,pot_dyn_handle)

sim.removeObjects([pot_handle,pot_dyn_handle])