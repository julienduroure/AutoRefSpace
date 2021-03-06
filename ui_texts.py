#
# AutoRefSpace is part of BleRiFa. http://BleRiFa.com
#
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
#	Copyright 2016-2018 Julien Duroure (contact@julienduroure.com)
#
##########################################################################################
ui_generated_text = '''# This file is auto-generated by addon AutoRefSpace
# http://BleRiFa.com/en/tools/AutoRefSpace
# for any questions, please ask contact@julienduroure.com
##########################################################################################
#
# AutoRefSpace is part of BleRiFa. http://BleRiFa.com
#
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
#	Copyright 2016-2018 Julien Duroure (contact@julienduroure.com)
#
##########################################################################################
import bpy

autorefspace_rig_id = "###rig_id###"

###ITEM_LISTS###

def cb_enum_items(self, context):
###ITEM_CHOICE###

###ITEMS_UPDATE_CB_LIST###

bpy.types.PoseBone.autorefspace_enum = bpy.props.EnumProperty(name = 'enum', items=cb_enum_items, update=cb_item_change)
bpy.types.Scene.juar_display_all = bpy.props.BoolProperty()

class POSE_PT_JuAR_AutoRefSpace_###rig_id###(bpy.types.Panel):
	bl_label = "###LABEL###"
	bl_space_type = 'VIEW_3D'
	bl_region_type = '###REGION_TYPE###'
	bl_category = "###CATEGORY###"

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and context.active_object.data.get("autorefspace_rig_id") is not None and context.active_object.data.get("autorefspace_rig_id") == autorefspace_rig_id and context.mode == 'POSE'


	def draw(self, context):
		layout = self.layout
		armature = context.object
		scene = context.scene

		refspace_tab = ###REFSPACE_TAB###
		enum_name = {
###ENUM_LABELS###
		}

		row = layout.row()
		row.prop(scene, "juar_display_all", text="Display All References")

		for bone in refspace_tab:
			if scene.juar_display_all == True or bone in [b.name for b in context.selected_pose_bones]:
				row = layout.row()
				row.prop(armature.pose.bones[bone], "autorefspace_enum", text=enum_name[bone])

def register():
	bpy.utils.register_class(POSE_PT_JuAR_AutoRefSpace_###rig_id###)

def unregister():
	bpy.utils.unregister_class(POSE_PT_JuAR_AutoRefSpace_###rig_id###)

register()
'''

call_back_text = '''
	matrix = context.object.convert_space(context.object.pose.bones[target_], context.object.pose.bones[target_].matrix, 'POSE', 'WORLD')
	for bone in tab:
		context.object.pose.bones[bone].matrix = context.object.convert_space(context.object.pose.bones[bone], matrix, 'WORLD', 'POSE')

    #store current keying set if any
	current_keying_set = context.scene.keying_sets.active_index

	# Set Keying set
	context.scene.keying_sets.active = context.scene.keying_sets_all['LocRotScale']

	# Store current selection
	current_selection = []
	for bone in context.object.data.bones:
		if bone.select == True:
			current_selection.append(bone.name)
			bone.select = False

	for bone in tab:
		context.object.data.bones[bone].select = True
		context.object.data.bones[bone].hide = False

	# Insert Keyframe
	bpy.ops.anim.keyframe_insert(type='__ACTIVE__')

	# Restore keyframe
	context.scene.keying_sets.active_index = current_keying_set

	#Restore selection
	for bone in context.object.data.bones:
		bone.select = False
		if bone.name in current_selection:
			bone.select = True

	for bone in tab:
		context.object.data.bones[bone].hide = True
'''


driver_generated_text = '''# This file is auto-generated by addon AutoRefSpace
# http://BleRiFa.com/en/tools/AutoRefSpace
# for any questions, please ask contact@julienduroure.com
##########################################################################################
#
# AutoRefSpace is part of BleRiFa. http://BleRiFa.com
#
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
#	Copyright 2016-2018 Julien Duroure (contact@julienduroure.com)
#
##########################################################################################
import bpy

'''
