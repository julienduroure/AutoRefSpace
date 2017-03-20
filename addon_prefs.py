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

from .globs import *

class JuAR_Preferences(bpy.types.AddonPreferences):
	bl_idname = __package__

	panel_name = bpy.props.StringProperty(name="Default Panel name", default="RefSpace")
	tab_tool   = bpy.props.StringProperty(name="Default Tab name", default="RefSpace")
	enum_label = bpy.props.StringProperty(name="Default Enum Label", default="RefSpace")

	sides = bpy.props.CollectionProperty(type=JuAR_SideItem)
	active_side = bpy.props.IntProperty()

	category = bpy.props.StringProperty(name="Category", default="AutoRefSpace", update=update_panel)

	def draw(self, context):
		layout = self.layout
		row_global = layout.row()

		row_global.prop(self, "juar_mode")

		row_global = layout.row()
		col = row_global.column()

		box = col.box()
		row = box.row()
		row.prop(self, "category", text="Addon tab")
		box = col.box()
		row = box.row()
		row.prop(self, "panel_name", text="Default Panel Name")
		row = box.row()
		row.prop(self, "tab_tool", text="Default Generated Tab")
		row = box.row()
		row.prop(self, "enum_label", text="Default Enum Label")

		col = row_global.column(align=True)
		row = col.row()

		if len(addonpref().sides) > 0:
			row.template_list("POSE_UL_JuAR_SideList", "", addonpref(), "sides", addonpref(), "active_side")

			col_ = row.column()
			row_ = col_.column(align=True)
			row_.operator("pose.juar_side_add", icon="ZOOMIN", text="")
			row_.operator("pose.juar_side_remove", icon="ZOOMOUT", text="")

			row_ = col_.column(align=True)
			row_.separator()
			row_.operator("pose.juar_side_move", icon='TRIA_UP', text="").direction = 'UP'
			row_.operator("pose.juar_side_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

		else:
			row.operator("pose.juar_side_init", text="Init sides, for mirror")



def register():
	bpy.utils.register_class(JuAR_SideItem)
	bpy.utils.register_class(JuAR_Preferences)

def unregister():
	bpy.utils.unregister_class(JuAR_SideItem)
	bpy.utils.unregister_class(JuAR_Preferences)
