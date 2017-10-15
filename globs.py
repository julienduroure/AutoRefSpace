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

import bpy

from .utils import *
from .ui import*

def update_panel(self, context):
	bpy.utils.unregister_class(POSE_PT_juar_AutoRefSpace_Limbs)
	bpy.utils.unregister_class(POSE_PT_juar_LimbDetail)
	bpy.utils.unregister_class(POSE_PT_juar_LiveAutoRefSpace)
	bpy.utils.unregister_class(POSE_PT_juar_LimbGenerate)

	POSE_PT_juar_AutoRefSpace_Limbs.bl_category = addonpref().category
	POSE_PT_juar_LimbDetail.bl_category = addonpref().category
	POSE_PT_juar_LiveAutoRefSpace.bl_category = addonpref().category
	POSE_PT_juar_LimbGenerate.bl_category = addonpref().category

	bpy.utils.register_class(POSE_PT_juar_AutoRefSpace_Limbs)
	bpy.utils.register_class(POSE_PT_juar_LimbDetail)
	bpy.utils.register_class(POSE_PT_juar_LiveAutoRefSpace)
	bpy.utils.register_class(POSE_PT_juar_LimbGenerate)

def cb_enum_items(self, context):
	items = []

	armature = context.object
	limb = armature.juar_limbs[armature.juar_active_limb]
	for bone in limb.ref_bones:
		if bone.name != "":
			items.append((bone.label, bone.label, ""))
	return items

def cb_enum_update(self, context):
	armature = context.object
	limb = armature.juar_limbs[armature.juar_active_limb]

	#store world location / rotation / scale of current bone
	matrix = armature.convert_space(armature.pose.bones[limb.bone_target], armature.pose.bones[limb.bone_target].matrix, 'POSE', 'WORLD')

	#activate default constraint (by setting influence to 1)
	for constr in armature.pose.bones[limb.bone_target].constraints:
		for bone in limb.ref_bones:
			if constr.name == bone.constraint:
				if bone.label == limb.enum:
					# restore matrix
					armature.pose.bones[bone.new_bone_name].matrix = armature.convert_space(armature.pose.bones[bone.new_bone_name], matrix, 'WORLD', 'POSE')
				else:
					pass

	for constr in armature.pose.bones[limb.bone_target].constraints:
		for bone in limb.ref_bones:
			if constr.name == bone.constraint:
				if bone.label == limb.enum:
					constr.influence = 1.0
				else:
					constr.influence = 0.0

def create_constraints(limb):
	armature = bpy.context.object

	set_active(limb.bone_target)
	cpt = 1
	for bone in limb.ref_bones:
		if bone.name == "":
			continue

		#create constraint
		transform_loc = armature.pose.bones[limb.bone_target].constraints.new(type="COPY_TRANSFORMS")
		transform_loc.target = armature
		transform_loc.subtarget = bone.new_bone_name
		name = "AutoRefSpace " + bone.name
		transform_loc.name = name

		#Move to top
		C = bpy.context.copy()
		C["constraint"] = transform_loc
		tab_size = len(armature.pose.bones[limb.bone].constraints)
		for i in range(cpt, tab_size):
			bpy.ops.constraint.move_up(C, constraint=transform_loc.name,owner='BONE')
		transform_loc.influence = 0.0
		bone.constraint = transform_loc.name
		cpt = cpt + 1

def cb_active_AutoRefSpace(self, context):
	armature = context.object
	limb = armature.juar_limbs[armature.juar_active_limb]


	if limb.active == True:

		#Set default label if needed
		for bone in limb.ref_bones:
			if bone.label == "":
				bone.label = bone.name

		#Store Parent
		bpy.ops.object.mode_set(mode='EDIT')
		if armature.data.edit_bones[limb.bone].parent:
			limb.parent = armature.data.edit_bones[limb.bone].parent.name
		else:
			limb.parent = ""

		# Create corresponding bones
		new_ = armature.data.edit_bones.new("juas_target_" + limb.bone)
		new_name = new_.name
		armature.data.edit_bones[new_name].head = armature.data.edit_bones[limb.bone].head
		armature.data.edit_bones[new_name].tail = armature.data.edit_bones[limb.bone].tail
		armature.data.edit_bones[new_name].roll = armature.data.edit_bones[limb.bone].roll
		limb.bone_target = new_name
		new_.parent = armature.data.edit_bones[limb.bone].parent

		armature.data.edit_bones[limb.bone].parent = new_
		for bone in limb.ref_bones:
			new_ = armature.data.edit_bones.new("juas_" + bone.name + "_" + limb.bone)
			new_name = new_.name
			armature.data.edit_bones[new_name].head = armature.data.edit_bones[limb.bone].head
			armature.data.edit_bones[new_name].tail = armature.data.edit_bones[limb.bone].tail
			armature.data.edit_bones[new_name].roll = armature.data.edit_bones[limb.bone].roll
			bone.new_bone_name = new_name
			new_.parent = armature.data.edit_bones[bone.name]
		bpy.ops.object.mode_set(mode='POSE')

		for bone in limb.ref_bones:
			armature.data.bones[bone.new_bone_name].hide_select = True
		armature.data.bones[limb.bone_target].hide_select = True

		# Create constraints
		create_constraints(limb)

		#activate default constraint (by setting influence to 1)
		for constr in armature.pose.bones[limb.bone_target].constraints:
			for bone in limb.ref_bones:
				if constr.name == bone.constraint:
					if bone.label == limb.enum:
						constr.influence = 1.0
					else:
						constr.influence = 0.0

	else:
		#first check to know if we are at initialisation of limb (when copy/copy mirror)
		if len([bone for bone in limb.ref_bones if bone.new_bone_name == ""]) != 0:
			return None

		#Reset parent of bone
		bpy.ops.object.mode_set(mode='EDIT')
		if limb.parent != "":
			armature.data.edit_bones[limb.bone].parent = armature.data.edit_bones[limb.parent]
		else:
			armature.data.edit_bones[limb.bone].parent = None
		limb.parent = ""
		bpy.ops.object.mode_set(mode='POSE')

		# delete bones
		bpy.ops.object.mode_set(mode='EDIT')
		for bone in limb.ref_bones:
			armature.data.edit_bones.remove(armature.data.edit_bones[bone.new_bone_name])
			bone.new_bone_name = ""
		armature.data.edit_bones.remove(armature.data.edit_bones[limb.bone_target])
		bpy.ops.object.mode_set(mode='POSE')


class JuAR_SideItem(bpy.types.PropertyGroup):
	name_R = bpy.props.StringProperty(name="Side name R")
	name_L = bpy.props.StringProperty(name="Side name L")

class BoneItem(bpy.types.PropertyGroup):
	name = bpy.props.StringProperty(name="Bone Name")
	label = bpy.props.StringProperty(name="Label")
	constraint = bpy.props.StringProperty(name="Label")
	new_bone_name = bpy.props.StringProperty(name="New bone name")

class LimbItem(bpy.types.PropertyGroup):

	name = bpy.props.StringProperty(name="Limb Name")
	active = bpy.props.BoolProperty(name="Active", update=cb_active_AutoRefSpace)
	generated = bpy.props.BoolProperty(name="Generated")
	enum_label = bpy.props.StringProperty(name="Enum Label")

	bone = bpy.props.StringProperty(name="Bone")
	parent = bpy.props.StringProperty(name="Parent")
	bone_target = bpy.props.StringProperty(name="Bone Target")

	ref_bones = bpy.props.CollectionProperty(type=BoneItem)
	active_ref_bone = bpy.props.IntProperty()

	enum = bpy.props.EnumProperty(name = 'enum', items=cb_enum_items, update=cb_enum_update)

	id = bpy.props.StringProperty(name="Id")

view_location_items = [
	("TOOLS", "Tools", "", 1),
	("UI", "Properties", "", 2),
]

class JuAR_Generation(bpy.types.PropertyGroup):
	view_location = bpy.props.EnumProperty(name="View location", items=view_location_items, default="TOOLS")
	panel_name    = bpy.props.StringProperty(name="Panel name")
	tab_tool      = bpy.props.StringProperty(name="Tab")

def register():
	bpy.utils.register_class(BoneItem)
	bpy.utils.register_class(LimbItem)
	bpy.utils.register_class(JuAR_Generation)

def unregister():
	bpy.utils.unregister_class(BoneItem)
	bpy.utils.unregister_class(LimbItem)
	bpy.utils.unregister_class(JuAR_Generation)
