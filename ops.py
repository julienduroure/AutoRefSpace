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

from .ui_texts import *
from .globs import *
from .utils import *
import uuid

class POSE_OT_juar_generate_refspace(bpy.types.Operator):
	"""Generate RefSpace"""
	bl_idname = "pose.juar_generate_refspace"
	bl_label = "Generate RefSpace"
	bl_options = {'REGISTER'}


	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juar_limbs) > 0 and context.mode == 'POSE'

	def execute(self, context):
		armature = context.active_object
		limbs = armature.juar_limbs

		for limb in limbs:
			#Do not generate already generated limbs
			if limb.generated == True:
				continue

			#Set default label if needed
			for bone in limb.ref_bones:
				if bone.label == "":
					bone.label = bone.name

			#Enable constraints or create them
			if limb.active == True:
				for bone in limb.ref_bones:
					if bone.name == "":
						continue
					armature.pose.bones[limb.bone].constraints.get(bone.constraint).mute = False
			else:
				#create constraints
				create_constraints(limb)

				#Delete parent
				bpy.ops.object.mode_set(mode='EDIT')
				if armature.data.edit_bones[limb.bone].parent:
					limb.parent = armature.data.edit_bones[limb.bone].parent.name
				else:
					limb.parent = ""
				armature.data.edit_bones[limb.bone].parent = None
				bpy.ops.object.mode_set(mode='POSE')

		if context.active_object.juar_generation.panel_name == "":
			context.active_object.juar_generation.panel_name =  addonpref().panel_name
		if context.active_object.juar_generation.tab_tool == "":
			context.active_object.juar_generation.tab_tool = addonpref().tab_tool

		#Add rig_id custom prop if not exists, and assign a random value
		if context.active_object.data.get('autorefspace_rig_id') is None:
			bpy.context.active_object.data['autorefspace_rig_id'] = uuid.uuid4().hex
		rig_id = context.active_object.data.get('autorefspace_rig_id')

		ui_generated_text_ = ui_generated_text
		ui_generated_text_ = ui_generated_text_.replace("###LABEL###", context.active_object.juar_generation.panel_name)
		ui_generated_text_ = ui_generated_text_.replace("###REGION_TYPE###", context.active_object.juar_generation.view_location)
		ui_generated_text_ = ui_generated_text_.replace("###CATEGORY###", context.active_object.juar_generation.tab_tool)
		ui_generated_text_ = ui_generated_text_.replace("###rig_id###", rig_id )

		#Create item lists
		txt = ""
		for limb in limbs:
			cpt = 1
			txt = txt + "items_" + limb.id + " = [\n"
			for bone in limb.ref_bones:
				if bone.name == "":
					continue
				txt = txt + "(\"" + bone.label + "\",\"" + bone.label + "\",\"\"," + str(cpt) + "),\n"
				cpt = cpt + 1
			txt = txt + "]\n"

		ui_generated_text_ = ui_generated_text_.replace("###ITEM_LISTS###", txt )

		#Create call back for choice of items
		txt = ""
		for limb in limbs:
			txt = txt + "\tif self.name == \"" + limb.bone + "\":\n"
			txt = txt + "\t\treturn items_" + limb.id + "\n"

		ui_generated_text_ = ui_generated_text_.replace("###ITEM_CHOICE###", txt )

		ui_generated_text_ = ui_generated_text_.replace("###REFSPACE_TAB###", str([limb.bone for limb in limbs]))

		#Create enum label dict
		txt = ""
		for limb in limbs:
			if limb.enum_label != "":
				txt = txt + "\"" + limb.bone + "\" : \"" + limb.enum_label + "\",\n"
			else:
				txt = txt + "\"" + limb.bone + "\" : \"" + addonpref().enum_label + "\",\n"

		ui_generated_text_ = ui_generated_text_.replace("###ENUM_LABELS###", txt)

		#Create UI file
		if context.active_object.data["autorefspace_rig_id"] + "_autorefspace_ui.py" in bpy.data.texts.keys():
			bpy.data.texts.remove(bpy.data.texts[context.active_object.data["autorefspace_rig_id"] + "_autorefspace_ui.py"])
		text = bpy.data.texts.new(name=context.active_object.data["autorefspace_rig_id"] + "_autorefspace_ui.py")
		text.use_module = True
		text.write(ui_generated_text_)
		exec(text.as_string(), {})

		#Create driver file
		txt = driver_generated_text
		for limb in limbs:
			txt = txt + "def driver_" + limb.id + "(label, enum):\n"
			txt = txt + "\treturn label == enum\n"
			txt = txt + "bpy.app.driver_namespace[\"driver_" + limb.id + "\"] =  driver_" + limb.id + "\n"

		if context.active_object.data["autorefspace_rig_id"] + "_autorefspace_drivers.py" in bpy.data.texts.keys():
			bpy.data.texts.remove(bpy.data.texts[context.active_object.data["autorefspace_rig_id"] + "_autorefspace_drivers.py"])
		text = bpy.data.texts.new(name=context.active_object.data["autorefspace_rig_id"] + "_autorefspace_drivers.py")
		text.use_module = True
		text.write(txt)
		exec(text.as_string(), {})

		#add drivers
		for limb in limbs:
			if limb.generated == True:
				continue
			cpt_enum = 1
			for bone in limb.ref_bones:
				if bone.name == "":
					continue
				fcurve = armature.pose.bones[limb.bone].constraints[cpt_enum-1].driver_add('influence')
				drv = fcurve.driver
				drv.type = 'SCRIPTED'
				drv.expression = "driver_" + limb.id + "(" + str(cpt_enum) + ", enum)"
				var = drv.variables.new()
				var.name = 'enum'
				var.type = 'SINGLE_PROP'
				targ = var.targets[0]
				targ.id = armature
				targ.data_path = "pose.bones[\"" + limb.bone + "\"].autorefspace_enum"
				cpt_enum = cpt_enum + 1

		for limb in limbs:
			if limb.generated == True:
				continue
			#Set default value
			armature.data.bones.active = armature.data.bones[limb.bone]
			if limb.ref_bones[limb.active_ref_bone].label != "":
				armature.pose.bones[limb.bone].autorefspace_enum = limb.ref_bones[limb.active_ref_bone].label
			else:
				for i in range(len(limb.ref_bones)):
					if limb.ref_bones[i].label != "":
						armature.pose.bones[limb.bone].autorefspace_enum = limb.ref_bones[i].label
						break

			#Set generate flag
			limb.generated = True

		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.object.mode_set(mode='POSE')


		return {'FINISHED'}

class POSE_OT_juar_update_refspace(bpy.types.Operator):
	"""Update RefSpace"""
	bl_idname = "pose.juar_update_refspace"
	bl_label = "Update RefSpace"
	bl_options = {'REGISTER'}


	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juar_limbs) > 0 and context.mode == 'POSE'

	def execute(self, context):
		armature = context.active_object
		limbs = armature.juar_limbs
		limb  = limbs[armature.juar_active_limb]

		#delete drivers
		for bone in limb.ref_bones:
			if bone.name == "":
				continue
			armature.pose.bones[limb.bone].constraints.get(bone.constraint).driver_remove('influence')

		#This will delete constraints
		limb.active = False

		#Delete keyframes on enum
		if bpy.context.active_object.animation_data and bpy.context.active_object.animation_data.action:
			curves = bpy.context.active_object.animation_data.action.fcurves
			for c in curves:
				if c.data_path.split('.')[len(c.data_path.split('.'))-1] == "autorefspace_enum":
					bpy.context.active_object.animation_data.action.fcurves.remove(c)
					break

		#Enable live ref space
		limb.generated = False

		return {'FINISHED'}


class POSE_OT_juar_limb_copy(bpy.types.Operator):
	"""Copy active system, with mirror option"""
	bl_idname = "pose.juar_limb_copy"
	bl_label = "Copy system"
	bl_options = {'REGISTER'}

	mirror = bpy.props.BoolProperty(name="Mirror", default=False)

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juar_limbs) > 0 and limb_check(context.active_object.juar_limbs[context.active_object.juar_active_limb]) == False

	def execute(self, context):

		if self.mirror == True:
			fct = get_symm_name
		else:
			fct = get_name

		if len(addonpref().sides) == 0:
			init_sides(context)

		armature = context.object
		src_limb_index = armature.juar_active_limb
		dst_limb = armature.juar_limbs.add()

		dst_limb.name = fct(armature.juar_limbs[src_limb_index].name)
		dst_limb.enum_label = armature.juar_limbs[src_limb_index].enum_label
		dst_limb.bone = fct(armature.juar_limbs[src_limb_index].bone)
		dst_limb.parent = fct(armature.juar_limbs[src_limb_index].parent)
		dst_limb.id = uuid.uuid4().hex

		for src_bone in armature.juar_limbs[src_limb_index].ref_bones:
			dst_bone = dst_limb.ref_bones.add()
			dst_bone.name = fct(src_bone.name)
			if src_bone.label != "":
				dst_bone.label = fct(src_bone.label)
			else:
				dst_bone.label = fct(src_bone.name)
			dst_bone.constraint = ""
		dst_limb.active_ref_bone = armature.juar_limbs[src_limb_index].active_ref_bone

		dst_limb.active = False
		dst_limb.generated = False

		armature.juar_active_limb = len(armature.juar_limbs) - 1

		return {'FINISHED'}


def register():
	bpy.utils.register_class(POSE_OT_juar_generate_refspace)
	bpy.utils.register_class(POSE_OT_juar_update_refspace)
	bpy.utils.register_class(POSE_OT_juar_limb_copy)

def unregister():
	bpy.utils.unregister_class(POSE_OT_juar_generate_refspace)
	bpy.utils.unregister_class(POSE_OT_juar_update_refspace)
	bpy.utils.unregister_class(POSE_OT_juar_limb_copy)
