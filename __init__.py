##########################################################################################
#	GPL LICENSE:
#-------------------------
# This file is part of AutoRefSpace.
# AutoRefSpace is part of http://BleRiFa.com
#
#    AutoRefSpace is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    AutoRefSpace is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with AutoRefSpace.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################################
#
#	Copyright 2016-2017 Julien Duroure (contact@julienduroure.com)
#
##########################################################################################

bl_info = {
	"name": "AutoRefSpace",
	"author": "Julien Duroure",
	"version": (0, 1, 0),
	"blender": (2,78, 0),
	"description": "Add RefSpace to your Bones",
	"location": "View 3D tools, tab 'AutoRefSpace'",
	"wiki_url": "http://blerifa.com/AutoRefSpace/",
	"tracker_url": "https://github.com/julienduroure/BleRiFa/issues/",
	"category": "Rigging",
}

if "bpy" in locals():
	import importlib
	importlib.reload(addon_prefs)
	importlib.reload(ui_texts)
	importlib.reload(globs)
	importlib.reload(utils)
	importlib.reload(ui)
	importlib.reload(ui_ops)
	importlib.reload(ops)
else:
	from .addon_prefs import *
	from .ui_texts import *
	from .globs import *
	from .utils import *
	from . import ui
	from . import ui_ops
	from . import ops

import bpy

def register():
	addon_prefs.register()
	globs.register()
	ops.register()
	ui_ops.register()
	ui.register()

	bpy.types.Object.juar_limbs = bpy.props.CollectionProperty(type=globs.LimbItem)
	bpy.types.Object.juar_active_limb = bpy.props.IntProperty()
	bpy.types.Object.juar_generation = bpy.props.PointerProperty(type=globs.JuAR_Generation)

def unregister():

	del bpy.types.Object.juar_limbs
	del bpy.types.Object.juar_active_limb
	del bpy.types.Object.juar_generation


	addon_prefs.unregister()
	globs.unregister()
	ops.unregister()
	ui_ops.unregister()
	ui.unregister()


if __name__ == "__main__":
	register()
