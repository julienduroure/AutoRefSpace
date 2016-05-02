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

def cb_enum_items(self, context):
	items = []
	
	armature = context.object
	limb = armature.juar_limbs[armature.juar_active_limb]
	for bone in limb.ref_bones:
		items.append((bone.label, bone.label, ""))
	return items
	
def cb_enum_update(self, context):
	armature = context.object
	limb = armature.juar_limbs[armature.juar_active_limb]
	for constr in armature.pose.bones[limb.bone].constraints:
		constr.influence = 0.0
	for constr in armature.pose.bones[limb.bone].constraints:
		found = False
		for bone in limb.ref_bones:
			if constr.name == bone.constraint and bone.label == limb.enum:
				constr.influence = 1.0
				found = True
				break
		if found == True:
			break
	
def cb_active_AutoRefSpace(self, context):
	armature = context.object
	limb = armature.juar_limbs[armature.juar_active_limb]
	
	if limb.active == True:
		#Store Parent
		bpy.ops.object.mode_set(mode='EDIT')
		limb.parent = armature.data.edit_bones[limb.bone].parent.name
		armature.data.edit_bones[limb.bone].parent = None
		bpy.ops.object.mode_set(mode='POSE')
		
		#Select and active bone, needed for set_inverse
		bpy.ops.pose.select_all(action='DESELECT')
		armature.data.bones[limb.bone].select = True
		armature.data.bones.active = armature.data.bones[limb.bone]
		cpt = 1
		for bone in limb.ref_bones:
			#If constraint already exists
			if armature.pose.bones[limb.bone].constraints.get(bone.constraint):
				armature.pose.bones[limb.bone].constraints.get(bone.constraint).mute = False
			#Create constraint
			else:
				#Create constraint
				childof = armature.pose.bones[limb.bone].constraints.new(type='CHILD_OF')
				childof.target = armature
				childof.subtarget = bone.name
				name = "AutoRefSpace " + bone.name
				childof.name = name
				
				#Move to top
				C = bpy.context.copy()
				C["constraint"] = childof
				tab_size = len(armature.pose.bones[limb.bone].constraints)
				for i in range(cpt, tab_size):
					bpy.ops.constraint.move_up(C, constraint=childof.name,owner='BONE')
				bpy.ops.constraint.childof_set_inverse(C, constraint=childof.name, owner='BONE')
				childof.influence = 0.0
				bone.constraint = childof.name
			cpt = cpt + 1
			
		#activate default constraint (by setting influence to 1)
		for constr in armature.pose.bones[limb.bone].constraints:
			constr.influence = 0.0
		for constr in armature.pose.bones[limb.bone].constraints:
			found = False
			for bone in limb.ref_bones:
				if constr.name == bone.constraint and bone.label == limb.enum:
					constr.influence = 1.0
					found = True
					break
			if found == True:
				break
			
		
	else:
		#Reset parent of bone
		bpy.ops.object.mode_set(mode='EDIT')
		armature.data.edit_bones[limb.bone].parent = armature.data.edit_bones[limb.parent]
		limb.parent = ""
		bpy.ops.object.mode_set(mode='POSE')
		
		#Mute all constraints
		for bone in limb.ref_bones:
			armature.pose.bones[limb.bone].constraints.get(bone.constraint).mute = True
		

class BoneItem(bpy.types.PropertyGroup):
	name = bpy.props.StringProperty(name="Bone Name")
	label = bpy.props.StringProperty(name="Label")
	constraint = bpy.props.StringProperty(name="Label")

class LimbItem(bpy.types.PropertyGroup):

	name = bpy.props.StringProperty(name="Limb Name")
	active = bpy.props.BoolProperty(name="Active", update=cb_active_AutoRefSpace)
	generated = bpy.props.BoolProperty(name="Generated")
	enum_label = bpy.props.StringProperty(name="Enum Label")
	
	bone = bpy.props.StringProperty(name="Bone")
	parent = bpy.props.StringProperty(name="Parent")
	
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
	
#shortcut to prefs
def addonpref():
	user_preferences = bpy.context.user_preferences
	return user_preferences.addons[__package__].preferences
	
def register():
	bpy.utils.register_class(BoneItem)
	bpy.utils.register_class(LimbItem)
	bpy.utils.register_class(JuAR_Generation)

def unregister():
	bpy.utils.unregister_class(BoneItem)
	bpy.utils.unregister_class(LimbItem)
	bpy.utils.unregister_class(JuAR_Generation)
