##########################################################################################
#	GPL LICENSE:
#-------------------------
# This file is part of AutoRefSpace.
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
#	Copyright 2016 Julien Duroure (contact@julienduroure.com)
#
##########################################################################################

bl_info = {
	"name": "AutoRefSpace",
	"author": "Julien Duroure",
	"version": (1, 0, 0),
	"blender": (2,77, 0),
	"description": "Add RefSpace to your Bones",
	"location": "View 3D tools, tab 'AutoRefSpace'",
	"wiki_url": "http://blerifa.com/AutoRefSpace/",
	"tracker_url": "https://github.com/julienduroure/AutoRefSpace/issues/",
	"category": "Rigging",
}

if "bpy" in locals():
	import imp
	imp.reload(addon_prefs)
	imp.reload(ui_texts)
	imp.reload(globals)
	imp.reload(utils)
	imp.reload(ui)
	imp.reload(ui_ops)
	imp.reload(ops)
else:
	from .addon_prefs import *
	from .ui_texts import *
	from .globals import *
	from .utils import *
	from . import ui
	from . import ui_ops
	from . import ops

import bpy

def register():
	addon_prefs.register()
	globals.register()
	ops.register()
	ui_ops.register()
	ui.register()

	bpy.types.Object.juar_generation = bpy.props.PointerProperty(type=JuAR_Generation)
	bpy.types.Object.juar_limbs = bpy.props.CollectionProperty(type=LimbItem)
	bpy.types.Object.juar_active_limb = bpy.props.IntProperty()

def unregister():
	addon_prefs.unregister()
	globals.unregister()
	ops.unregister()
	ui_ops.unregister()
	ui.unregister()

	del bpy.types.Object.juar_limbs
	del bpy.types.Object.juar_active_limb

if __name__ == "__main__":
	register()
