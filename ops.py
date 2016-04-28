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
import uuid

class POSE_OT_juar_generate_refspace(bpy.types.Operator):
	"""Generate RefSpace"""
	bl_idname = "pose.juas_generate_refspace"
	bl_label = "Generate RefSpace"
	bl_options = {'REGISTER'}
	
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juar_limbs) > 0 and context.mode == 'POSE'
		
	def execute(self, context):
		armature = context.active_object
		limbs = armature.juar_limbs
		
		for limb in limbs:
			for bone in limb.ref_bones:
				armature.pose.bones[limb.bone].constraints.get(bone.constraint).mute = False
			bpy.ops.object.mode_set(mode='EDIT')
			armature.data.edit_bones[limb.bone].parent = None
			bpy.ops.object.mode_set(mode='POSE')
		
		if context.active_object.juar_generation.panel_name == "":
			context.active_object.juar_generation.panel_name = "test" #addonpref().panel_name #TODO
		if context.active_object.juar_generation.tab_tool == "":
			context.active_object.juar_generation.tab_tool = "test" # addonpref().tab_tool #TODO
		
		#Add rig_id custom prop if not exists, and assign a random value
		if context.active_object.data.get('autorefspace_rig_id') is None:
			bpy.context.active_object.data['autorefspace_rig_id'] = uuid.uuid4().hex
		rig_id = context.active_object.data.get('autorefspace_rig_id')
		
		ui_generated_text_ = ui_generated_text
		ui_generated_text_ = ui_generated_text_.replace("###LABEL###", context.active_object.juar_generation.panel_name) 
		ui_generated_text_ = ui_generated_text_.replace("###REGION_TYPE###", context.active_object.juar_generation.view_location) 
		ui_generated_text_ = ui_generated_text_.replace("###CATEGORY###", context.active_object.juar_generation.tab_tool)
		ui_generated_text_ = ui_generated_text_.replace("###rig_id###", rig_id )
		
		txt = ""
		for limb in limbs:
			cpt = 1
			txt = txt + limb.id + "_items = [\n"
			for bone in limb.ref_bones:
				txt = txt + "(\"" + bone.label + "\",\"" + bone.label + "\",\"\"," + str(cpt) + "),\n"
				cpt = cpt + 1
			txt = txt + "]\n"
			
		ui_generated_text_ = ui_generated_text_.replace("###ITEM_LISTS###", txt )
		
		txt = ""
		for limb in limbs:
			txt = txt + "\tif context.active_pose_bone.name == \"" + limb.bone + "\":\n"
			txt = txt + "\t\treturn " + limb.id + "_items\n"
			
		ui_generated_text_ = ui_generated_text_.replace("###ITEM_CHOICE###", txt )
		
		ui_generated_text_ = ui_generated_text_.replace("###REFSPACE_TAB###", str([limb.bone for limb in limbs]))
		
		if context.active_object.data["autorefspace_rig_id"] + "_autorefspace_ui.py" in bpy.data.texts.keys():
			bpy.data.texts.remove(bpy.data.texts[context.active_object.data["autorefspace_rig_id"] + "_autorefspace_ui.py"])
		text = bpy.data.texts.new(name=context.active_object.data["autorefspace_rig_id"] + "_autorefspace_ui.py")
		text.use_module = True
		text.write(ui_generated_text_)
		exec(text.as_string(), {})
			
		txt = "import bpy\n"
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
			cpt_enum = 1
			for bone in limb.ref_bones:
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
		
		#TODO : delete limb
		#TODO : set default value
		
		return {'FINISHED'}

def register():
	bpy.utils.register_class(POSE_OT_juar_generate_refspace)
	
def unregister():
	bpy.utils.unregister_class(POSE_OT_juar_generate_refspace)