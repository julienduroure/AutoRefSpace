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
import uuid

from .globs import *
from .utils import *

class POSE_OT_juar_limb_select_bone(bpy.types.Operator):
	"""Set active bone to system bone"""
	bl_idname = "pose.juar_limb_select_bone"
	bl_label = "Select system bone"
	bl_options = {'REGISTER'}

	bone = bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juar_limbs) > 0 and context.mode == 'POSE'

	def execute(self, context):
		armature = context.object
		if context.active_pose_bone:
			bone_name = context.active_pose_bone.name

		if self.bone == "bone":
			armature.juar_limbs[armature.juar_active_limb][self.bone] = bone_name
		elif self.bone == "active_ref_bone":
			armature.juar_limbs[armature.juar_active_limb].ref_bones[armature.juar_limbs[armature.juar_active_limb].active_ref_bone].name = bone_name
			armature.juar_limbs[armature.juar_active_limb].ref_bones[armature.juar_limbs[armature.juar_active_limb].active_ref_bone].label = bone_name

		return {'FINISHED'}



class POSE_OT_juar_limb_move(bpy.types.Operator):
	"""Move system up or down in the list"""
	bl_idname = "pose.juar_limb_move"
	bl_label = "Move system"
	bl_options = {'REGISTER'}

	direction = bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juar_limbs) > 0

	def execute(self, context):
		armature = context.object
		index   = armature.juar_active_limb

		if self.direction == "UP":
			new_index = index - 1
		elif self.direction == "DOWN":
			new_index = index + 1
		else:
			new_index = index

		if new_index < len(armature.juar_limbs) and new_index >= 0:
			armature.juar_limbs.move(index, new_index)
			armature.juar_active_limb = new_index

		return {'FINISHED'}

class POSE_OT_juar_limb_add(bpy.types.Operator):
	"""Add a new system"""
	bl_idname = "pose.juar_limb_add"
	bl_label = "Add system"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE"

	def execute(self, context):
		armature = context.object

		if len(addonpref().sides) == 0:
			init_sides(context)

		limb = armature.juar_limbs.add()
		if context.active_pose_bone:
			limb.name = ("Limb.%d" + get_side(context.active_pose_bone.name)) % len(armature.juar_limbs)
		else:
			limb.name = "Limb.%d" % len(armature.juar_limbs)
		limb.id = uuid.uuid4().hex

		armature.juar_active_limb = len(armature.juar_limbs) - 1

		#Autofill with selection / active
		if len(context.selected_pose_bones) != 0:
			for bone in context.selected_pose_bones:
				if bone.name == context.active_pose_bone.name:
					limb.bone = bone.name
				else:
					ref = limb.ref_bones.add()
					ref.name  = bone.name
					ref.label = bone.name
					limb.active_ref_bone = len(limb.ref_bones) - 1
					if len(limb.ref_bones) == 1:
						# At creation, setting the first one as default in enum
						ref.enum_default = True

		return {'FINISHED'}

class POSE_OT_juar_limb_remove(bpy.types.Operator):
	"""Remove the current system"""
	bl_idname = "pose.juar_limb_remove"
	bl_label = "Remove system"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		if context.active_object and context.active_object.type == "ARMATURE" and context.active_object.juar_active_limb >= 0:
			try:
				return context.active_object.juar_limbs[context.active_object.juar_active_limb].active == False and context.active_object.juar_limbs[context.active_object.juar_active_limb].generated == False
			except:
				return False

	def execute(self, context):
		armature = context.object
		limb = armature.juar_limbs[armature.juar_active_limb]

		armature.juar_limbs.remove(armature.juar_active_limb)
		len_ = len(armature.juar_limbs)
		if (armature.juar_active_limb > (len_ - 1) and len_ > 0):
			armature.juar_active_limb = len(armature.juar_limbs) - 1


		return {'FINISHED'}

class POSE_OT_juar_ref_bone_move(bpy.types.Operator):
	"""Move bone up or down in the list"""
	bl_idname = "pose.juar_ref_bone_move"
	bl_label = "Move Bone"
	bl_options = {'REGISTER'}

	direction = bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juar_limbs) > 0 and len(context.object.juar_limbs[context.object.juar_active_limb].ref_bones) > 0

	def execute(self, context):
		armature = context.object
		index_limb  = armature.juar_active_limb
		index_bone  = armature.juar_limbs[index_limb].active_ref_bone

		if self.direction == "UP":
			new_index = index_bone - 1
		elif self.direction == "DOWN":
			new_index = index_bone + 1
		else:
			new_index = index_bone

		if new_index < len(armature.juar_limbs[index_limb].ref_bones) and new_index >= 0:
			armature.juar_limbs[index_limb].ref_bones.move(index_bone, new_index)
			armature.juar_limbs[index_limb].active_ref_bone = new_index

		return {'FINISHED'}

class POSE_OT_juar_ref_bone_add(bpy.types.Operator):
	"""Add a new Bone"""
	bl_idname = "pose.juar_ref_bone_add"
	bl_label = "Add Bone"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juar_limbs) > 0

	def execute(self, context):
		armature = context.object
		index_limb = armature.juar_active_limb

		bone = armature.juar_limbs[index_limb].ref_bones.add()
		if context.active_pose_bone:
			bone.name  = context.active_pose_bone.name
			bone.label = context.active_pose_bone.name
			if len(armature.juar_limbs[index_limb].ref_bones) == 1:
				# At creation, the first one is default in enum
				bone.enum_default = True
		armature.juar_limbs[index_limb].active_ref_bone = len(armature.juar_limbs[index_limb].ref_bones) - 1

		return {'FINISHED'}

class POSE_OT_juar_ref_bone_remove(bpy.types.Operator):
	"""Remove the current Bone"""
	bl_idname = "pose.juar_ref_bone_remove"
	bl_label = "Remove Bone"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juar_limbs) > 0 and len(context.object.juar_limbs[context.object.juar_active_limb].ref_bones) > 0

	def execute(self, context):
		armature = context.object
		index_limb = armature.juar_active_limb
		index_bone = armature.juar_limbs[index_limb].active_ref_bone

		armature.juar_limbs[index_limb].ref_bones.remove(armature.juar_limbs[index_limb].active_ref_bone)
		len_ = len(armature.juar_limbs[index_limb].ref_bones)
		if (armature.juar_limbs[index_limb].active_ref_bone > (len_ - 1) and len_ > 0):
			armature.juar_limbs[index_limb].active_ref_bone = len(armature.juar_limbs[index_limb].ref_bones) - 1

		return {'FINISHED'}

class POSE_OT_juar_limb_select_bone_from_selection(bpy.types.Operator):
	"""Set selected bones to collection"""
	bl_idname = "pose.juar_limb_selected_bones_select"
	bl_label = "Add selected bones"
	bl_options = {'REGISTER'}

	bone = bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juar_limbs) > 0 and context.mode == 'POSE'

	def execute(self, context):
		armature = context.object
		selected = context.selected_pose_bones

		if self.bone == "ref_bones":
			for bone in selected:
				if bone.name not in [ref.name for ref in armature.juar_limbs[armature.juar_active_limb].ref_bones]:
					new_bone = armature.juar_limbs[armature.juar_active_limb].ref_bones.add()
					new_bone.name = bone.name
					new_bone.label = bone.name
					if len(armature.juar_limbs[armature.juar_active_limb].ref_bones) == 1:
						new_bone.enum_default = True
					armature.juar_limbs[armature.juar_active_limb].active_ref_bone = len(armature.juar_limbs[armature.juar_active_limb].ref_bones) - 1

		return {'FINISHED'}

class POSE_OT_juar_side_move(bpy.types.Operator):
	"""Move Side up or down in the list"""
	bl_idname = "pose.juar_side_move"
	bl_label = "Move Side"
	bl_options = {'REGISTER'}

	direction = bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(addonpref().sides) > 0

	def execute(self, context):
		index   = addonpref().active_side

		if self.direction == "UP":
			new_index = index - 1
		elif self.direction == "DOWN":
			new_index = index + 1
		else:
			new_index = index

		if new_index < len(addonpref().sides) and new_index >= 0:
			addonpref().sides.move(index, new_index)
			addonpref().active_side = new_index

		return {'FINISHED'}

class POSE_OT_juar_side_add(bpy.types.Operator):
	"""Add a new Side"""
	bl_idname = "pose.juar_side_add"
	bl_label = "Add Side"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE"

	def execute(self, context):
		side = addonpref().sides.add()
		side.name = "Side.%d" % len(addonpref().sides)
		addonpref().active_side = len(addonpref().sides) - 1

		return {'FINISHED'}

class POSE_OT_juar_side_remove(bpy.types.Operator):
	"""Remove the current Side"""
	bl_idname = "pose.juar_side_remove"
	bl_label = "Remove Side"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE"

	def execute(self, context):
		addonpref().sides.remove(addonpref().active_side)
		len_ = len(addonpref().sides)
		if (addonpref().active_side > (len_ - 1) and len_ > 0):
			addonpref().active_side = len(addonpref().sides) - 1

		return {'FINISHED'}


class POSE_OT_juar_side_init(bpy.types.Operator):
	"""Init Side"""
	bl_idname = "pose.juar_side_init"
	bl_label = "Init Side"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return True

	def execute(self, context):
		init_sides(context)

		return {'FINISHED'}

class POSE_OT_juar_default_enum(bpy.types.Operator):
	"""Set default enum value"""
	bl_idname = "pose.juar_default_enum"
	bl_label = "Set default enum value"
	bl_options = {'REGISTER'}

	idx = bpy.props.IntProperty()

	@classmethod
	def poll(self, context):
		return True

	def execute(self, context):
		armature = context.object
		for bone in armature.juar_limbs[armature.juar_active_limb].ref_bones:
			bone.enum_default = False
		armature.juar_limbs[armature.juar_active_limb].ref_bones[self.idx].enum_default = True
		return {'FINISHED'}

def register():

	bpy.utils.register_class(POSE_OT_juar_limb_move)
	bpy.utils.register_class(POSE_OT_juar_limb_add)
	bpy.utils.register_class(POSE_OT_juar_limb_remove)

	bpy.utils.register_class(POSE_OT_juar_ref_bone_move)
	bpy.utils.register_class(POSE_OT_juar_ref_bone_add)
	bpy.utils.register_class(POSE_OT_juar_ref_bone_remove)

	bpy.utils.register_class(POSE_OT_juar_limb_select_bone)
	bpy.utils.register_class(POSE_OT_juar_limb_select_bone_from_selection)

	bpy.utils.register_class(POSE_OT_juar_side_move)
	bpy.utils.register_class(POSE_OT_juar_side_add)
	bpy.utils.register_class(POSE_OT_juar_side_remove)
	bpy.utils.register_class(POSE_OT_juar_side_init)

	bpy.utils.register_class(POSE_OT_juar_default_enum)

def unregister():

	bpy.utils.unregister_class(POSE_OT_juar_limb_move)
	bpy.utils.unregister_class(POSE_OT_juar_limb_add)
	bpy.utils.unregister_class(POSE_OT_juar_limb_remove)

	bpy.utils.unregister_class(POSE_OT_juar_ref_bone_move)
	bpy.utils.unregister_class(POSE_OT_juar_ref_bone_add)
	bpy.utils.unregister_class(POSE_OT_juar_ref_bone_remove)

	bpy.utils.unregister_class(POSE_OT_juar_limb_select_bone)
	bpy.utils.unregister_class(POSE_OT_juar_limb_select_bone_from_selection)

	bpy.utils.unregister_class(POSE_OT_juar_side_move)
	bpy.utils.unregister_class(POSE_OT_juar_side_add)
	bpy.utils.unregister_class(POSE_OT_juar_side_remove)
	bpy.utils.unregister_class(POSE_OT_juar_side_init)

	bpy.utils.unregister_class(POSE_OT_juar_default_enum)
