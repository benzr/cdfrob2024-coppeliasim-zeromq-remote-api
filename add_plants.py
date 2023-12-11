import os
import math
import numpy as np
import random
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
# if RemoteAPIClient import fails, install with : 
# python3 -m pip install coppeliasim-zmqremoteapi-client

client = RemoteAPIClient()
sim = client.require('sim')
sim.setStepping(False)


# change dir_path_stl to your own path if needed 
dir_path_stl = os.path.join(os.getcwd(),"3D_FINALE_V1/stl/")
file_format = 0 # auto detect format
file_name = os.path.join(dir_path_stl,'plante_haut_LR.stl')
options = 16 # tries to preserve textures
identical_vertice_tolerance = 0.0 # default
scaling_factor = 0.001 # mm to m
plante_top_handle = sim.importShape(file_format, file_name, options, 
                               identical_vertice_tolerance, scaling_factor)
sim.setObjectAlias(plante_top_handle, "plante top")
# in case we need the shape to do some computations, 
# we can get the vertices and the indices of the faces
options = 0
vertices_top, indices_top = sim.importMesh(file_format, file_name, options,
                                   identical_vertice_tolerance, scaling_factor)

sim.setObjectColor (plante_top_handle,0,sim.colorcomponent_ambient_diffuse,[0.0,0.8,0.2])
sim.setObjectColor(plante_top_handle, 0, sim.colorcomponent_specular, [0.1, 0.1, 0.1])

file_name = os.path.join(dir_path_stl,'plante_bas_LR.stl')
options = 16 # tries to preserve textures
plante_bot_handle = sim.importShape(file_format, file_name, options, 
                               identical_vertice_tolerance, scaling_factor)
sim.setObjectColor (plante_bot_handle,0,sim.colorcomponent_ambient_diffuse,[0.3,0.2,0.0])
sim.setObjectColor(plante_bot_handle, 0, sim.colorcomponent_specular, [0.1, 0.1, 0.1])
sim.setObjectAlias(plante_bot_handle, "plante bot")
options = 0
vertices_bot, indices_bot = sim.importMesh(file_format, file_name, options,
                                   identical_vertice_tolerance, scaling_factor)


dir_path_stl = os.path.join(os.getcwd(),"stl_FINALE_V1/")
file_name = os.path.join(dir_path_stl,'Pot_Plante.stl')
dir_path_stl = os.path.join(os.getcwd(),"3D_FINALE_V1/stl/")
file_name = os.path.join(dir_path_stl,'Pot_Plante_LR.stl')
options = 0
vertices, indices = sim.importMesh(file_format, file_name, options,
                                   identical_vertice_tolerance, scaling_factor)
decimation = 1.0 # 1.0 no decimation, 0.0 full decimation all facets removed
if decimation < 1.0:
    print (len(vertices[0]),len(indices[0]))
    vertices_out, indices_out = sim.getDecimatedMesh(vertices[0], indices[0], 1.0) 
    print (len(vertices_out),len(indices_out))
else:
    vertices_out = vertices[0]
    indices_out = indices[0]
plant_base_handle = sim.createShape(0, math.radians(20), vertices_out, indices_out)
sim.setObjectColor(plant_base_handle, 0, sim.colorcomponent_ambient_diffuse, [0.25, 0.0, 0.6])
sim.setObjectColor(plant_base_handle, 0, sim.colorcomponent_specular, [0.1, 0.1, 0.1])
sim.scaleObject(plant_base_handle, 1.15, 1.05, 1.05, 0)
sim.setObjectAlias(plant_base_handle, "plante base")

# copy plant elements before grouping 
copy_handles = sim.copyPasteObjects([plant_base_handle, plante_top_handle, plante_bot_handle],0)
# group to make plant 1
plante_a_handle = sim.groupShapes([plant_base_handle, plante_top_handle, plante_bot_handle], False)
sim.setObjectAlias(plante_a_handle, "plante A 00")

plante_b_handle = copy_handles[0]
plante_top_b_handle = copy_handles[1]
plante_bot_b_handle = copy_handles[2]
sim.setObjectColor(plante_b_handle, 0, sim.colorcomponent_ambient_diffuse, [0.9, 0.9, 0.9])
sim.setObjectColor (plante_top_b_handle,0,sim.colorcomponent_ambient_diffuse,[0.0,0.35,0.05])
plante_b_handle = sim.groupShapes([plante_b_handle, plante_top_b_handle, plante_bot_b_handle], False)
sim.setObjectAlias(plante_b_handle, "plante B 00")

options = 0
plant_dyn_handle =  sim.createPrimitiveShape(sim.primitiveshape_cylinder, 
                                        [0.05, 0.05, 0.1], options)
sim.setObjectPosition (plant_dyn_handle, [0,0,0.1/2], plant_dyn_handle)
prop = sim.objectspecialproperty_collidable 
prop += sim.objectspecialproperty_measurable
prop += sim.objectspecialproperty_detectable
sim.setObjectInt32Param(plant_dyn_handle,sim.shapeintparam_respondable,1) # respondable
sim.setObjectInt32Param(plant_dyn_handle,sim.shapeintparam_static,0) # dynamic
sim.setObjectInt32Param(plant_dyn_handle,sim.objintparam_visibility_layer,0) # non visible
sim.setObjectSpecialProperty(plant_dyn_handle, prop) # usable by all sensors

# save the dynamic object for tutorial
vertices, indices, normals = sim.getShapeMesh(plant_dyn_handle)
file_name = os.path.join(dir_path_stl,'plant_dyn_mesh.stl')
options = 0
format_type = 4 # STL binary
scaling_factor = 1000 # to mm
#data = sim.getShapeViz(plant_dyn_handle,0)
#print (len(data["indices"]),len(indices))
sim.exportMesh(format_type,file_name,options,scaling_factor,[vertices],[indices])

def rand6 ():
    s = []
    for i in range(6):
        s.append(random.uniform(0.0,1.0))
    return sorted(range(len(s)), key=lambda k: s[k])


v_xc = [0.5, 0.0, -0.5, -0.5, 0.0, 0.5]
v_yc = [0.3, 0.5, 0.3, -0.3, -0.5, -0.3]
bounding_box = sim.getShapeBB(plant_dyn_handle)
zc = bounding_box[2]/2.0
v_ang = np.linspace(0,300,6)
r = 0.08
plant_num_a = 0
plant_num_b = 0
for i in range(6):
    xc = v_xc[i]
    yc = v_yc[i]
    vk = rand6()
    k = 0
    for j in range(2):
        ang = np.radians(v_ang[vk[k]])
        k+=1
        x = xc + r*np.cos(ang)
        y = yc + r*np.sin(ang)
        z = zc
        plant_num_a+=1
        copy_handles = sim.copyPasteObjects([plante_a_handle,plant_dyn_handle], 0)
        keep_in_place = True
        sim.setObjectParent(copy_handles[0],copy_handles[1],keep_in_place)        
        sim.setObjectPosition (copy_handles[1], [x,y,z], copy_handles[1])
        object_name = "plante A %2.2d"%(plant_num_a)
        sim.setObjectAlias(copy_handles[0], object_name)
        object_name = "plante dyn A %2.2d"%(plant_num_a)
        sim.setObjectAlias(copy_handles[1], object_name)
    for j in range(4):
        ang = np.radians(v_ang[vk[k]])
        k+=1
        x = xc + r*np.cos(ang)
        y = yc + r*np.sin(ang)
        z = zc
        plant_num_b+=1
        copy_handles = sim.copyPasteObjects([plante_b_handle,plant_dyn_handle], 0)
        keep_in_place = True
        sim.setObjectParent(copy_handles[0],copy_handles[1],keep_in_place)   
        sim.setObjectPosition (copy_handles[1], [x,y,z], copy_handles[1])
        object_name = "plante B %2.2d"%(plant_num_b)
        sim.setObjectAlias(copy_handles[0], object_name)
        object_name = "plante dyn B %2.2d"%(plant_num_b)
        sim.setObjectAlias(copy_handles[1], object_name)

sim.removeObjects([plante_a_handle])
sim.removeObjects([plante_b_handle])
sim.removeObjects([plant_dyn_handle])