import os
import math
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
# if RemoteAPIClient import fails, install with : 
# python3 -m pip install coppeliasim-zmqremoteapi-client

client = RemoteAPIClient()
sim = client.require('sim')
sim.setStepping(False)

# remove default floor
try:
    floor_box_handle = sim.getObject("/Floor/box")
    floor_handle = sim.getObject("/Floor")
    sim.removeObjects([floor_box_handle,floor_handle])
except:
    print ("Default Floor already removed ...")

# change dir_path_stl to your own path if needed 
dir_path_stl = os.path.join(os.getcwd(),"3D_FINALE_V1/stl/")
file_format = 0 # auto detect format
file_name = os.path.join(dir_path_stl,'table_2024.stl')
options = 16 # tries to preserve textures
identical_vertice_tolerance = 0.0 # default
scaling_factor = 0.001 # mm to m
table_handle = sim.importShape(file_format, file_name, options, 
                               identical_vertice_tolerance, scaling_factor)
sim.setObjectAlias(table_handle, "table 2024")
# in case we need the shape to do some computations, 
# we can get the vertices and the indices of the faces
options = 0
vertices, indices = sim.importMesh(file_format, file_name, options,
                                   identical_vertice_tolerance, scaling_factor)

# add the texture on the floor
dir_path_textures = os.path.join(os.getcwd(),"vinyle_FINALE_V1")
file_name = os.path.join(dir_path_textures,
                         'vinyle_table_2024_FINAL_V1.svg')
options = 0
plane_sizes = [3.0,2.0]
scaling_UV = [3.0,3.0]
xy_g = [0,0,math.radians(180)] # or [0,0,0]
fixed_resolution = 0    
resolution = None
tapis_handle, id, res = sim.createTexture(file_name, options,
                            plane_sizes, scaling_UV, xy_g, 
                            fixed_resolution, resolution)
sim.setObjectAlias(tapis_handle, "tapis")
sim.setObjectPosition(tapis_handle, [0,0,0.0005],
                      sim.handle_world)
sim.setObjectInt32Param(tapis_handle,
                        sim.shapeintparam_respondable,1)

# respondable static walls
options = 0
walls_handles = []
wall1_handle = sim.createPrimitiveShape(sim.primitiveshape_cuboid, [3.04, 0.02, 0.15], options)
walls_handles.append(wall1_handle)
sim.setObjectAlias(wall1_handle, "wall1")
sim.setObjectPosition(wall1_handle, [0,1.01,0], sim.handle_world)
wall2_handle = sim.createPrimitiveShape(sim.primitiveshape_cuboid, [3.04, 0.02, 0.15], options)
walls_handles.append(wall2_handle)
sim.setObjectAlias(wall2_handle, "wall2")
sim.setObjectPosition(wall2_handle, [0,-1.01,0], sim.handle_world)
wall3_handle = sim.createPrimitiveShape(sim.primitiveshape_cuboid, [2.0, 0.02, 0.15], options)
walls_handles.append(wall3_handle)
sim.setObjectAlias(wall3_handle, "wall3")
sim.setObjectPosition(wall3_handle, [1.51,0,0], sim.handle_world)
sim.setObjectOrientation(wall3_handle, [0,0,math.pi/2],wall3_handle)
wall4_handle = sim.createPrimitiveShape(sim.primitiveshape_cuboid, [2.0, 0.02, 0.15], options)
walls_handles.append(wall4_handle)
sim.setObjectAlias(wall4_handle, "wall4")
sim.setObjectPosition(wall4_handle, [-1.51,0,0], sim.handle_world)
sim.setObjectOrientation(wall4_handle, [0,0,math.pi/2],wall4_handle)
prop = sim.objectspecialproperty_collidable 
prop += sim.objectspecialproperty_measurable
prop += sim.objectspecialproperty_detectable
for wall_handle in walls_handles:
    sim.setObjectInt32Param(wall_handle,sim.shapeintparam_respondable,1) # respondable
    sim.setObjectInt32Param(wall_handle,sim.shapeintparam_static,1) # static
    sim.setObjectInt32Param(wall_handle,sim.objintparam_visibility_layer,0) # non visible
    sim.setObjectSpecialProperty(wall_handle, prop) # usable by all sensors



