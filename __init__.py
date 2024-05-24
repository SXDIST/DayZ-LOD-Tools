bl_info = {
    "name" : "Arma 3 Object Builder Extensions",
    "description" : "A set of usefull extensions for Arma 3 Object Builder addon",
    "author" : "Mikk, SXDIST",
    "blender" : (2, 80, 0),
    "category" : "3D View"
}

from . import auto_load

auto_load.init()

def register():
    auto_load.register()

def unregister():
    auto_load.unregister()
