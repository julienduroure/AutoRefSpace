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

import bpy

from .globals import *

class JuAR_Preferences(bpy.types.AddonPreferences):
	bl_idname = __package__

	panel_name = bpy.props.StringProperty(name="Default Panel name", default="RefSpace")
	tab_tool   = bpy.props.StringProperty(name="Default Tab name", default="RefSpace")
	enum_label = bpy.props.StringProperty(name="Default Enum Label", default="RefSpace")
	
	def draw(self, context):
		layout = self.layout
		row = layout.row()
		layout.prop(self, "panel_name", text="Default Panel Name")
		row = layout.row()
		layout.prop(self, "tab_tool", text="Default Tab")
		row = layout.row()
		layout.prop(self, "enum_label", text="Default Enum Label")
		
def register():
	bpy.utils.register_class(JuAR_Preferences)

def unregister():
	bpy.utils.unregister_class(JuAR_Preferences)
