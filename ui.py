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


class POSE_UL_JuAR_SideList(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			layout.prop(item, "name_L", text="", emboss=False)
			layout.prop(item, "name_R", text="", emboss=False)
			
		elif self.layout_type in {'GRID'}:
			layout.alignment = 'CENTER'	

class POSE_UL_juar_LimbList(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			layout.prop(item, "name", text="", emboss=False)
			
		elif self.layout_type in {'GRID'}:
			layout.alignment = 'CENTER'
			
class POSE_UL_juar_BoneList(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			layout.prop(item, "name", text="", emboss=False)
			
		elif self.layout_type in {'GRID'}:
			layout.alignment = 'CENTER'
			
class POSE_PT_juar_AutoRefSpace_Limbs(bpy.types.Panel):
	bl_label = "Limbs"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "AutoRefSpace"	
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and context.mode == 'POSE'
		
	def draw(self, context):
		layout = self.layout
		armature = context.object
		
		row = layout.row()
		row.template_list("POSE_UL_juar_LimbList", "", armature, "juar_limbs", armature, "juar_active_limb")
		
		col = row.column()
		row = col.column(align=True)
		row.operator("pose.juar_limb_add", icon="ZOOMIN", text="")
		row.operator("pose.juar_limb_remove", icon="ZOOMOUT", text="")
		row.menu("POSE_MT_JuAR_limb_specials", icon='DOWNARROW_HLT', text="")
			
		if len(context.active_object.juar_limbs) > 0:
			row = col.column(align=True)
			row.separator()
			row.operator("pose.juar_limb_move", icon='TRIA_UP', text="").direction = 'UP'
			row.operator("pose.juar_limb_move", icon='TRIA_DOWN', text="").direction = 'DOWN'			
			
class POSE_PT_juar_LimbDetail(bpy.types.Panel):
	bl_label = "Limb Detail"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "AutoRefSpace"	
	
	@classmethod
	def poll(self, context):
		armature = context.active_object
		return armature and armature.type == "ARMATURE" and len(armature.juar_limbs) > 0 and context.mode == 'POSE' and armature.juar_limbs[armature.juar_active_limb].active == False and armature.juar_limbs[armature.juar_active_limb].generated == False
		
	def draw(self, context):
		layout = self.layout
		armature = context.object
		limb = armature.juar_limbs[armature.juar_active_limb]
		
		row = layout.row()
		row.prop(limb, "enum_label", text="Label")
		row = layout.row()
		col = row.column()
		row_ = col.column(align=True)
		row_.prop_search(limb, "bone", armature.data, "bones", text="Bone")
		col = row_.column()
		row_ = col.column(align=True)
		op = row.operator("pose.juar_limb_select_bone", icon="BONE_DATA", text="")
		op.bone = "bone"
		
		row = layout.row()
		op = row.operator("pose.juar_limb_selected_bones_select", text="Fill from selection")
		op.bone = "ref_bones"
		row = layout.row()
		row.template_list("POSE_UL_juar_BoneList", "", limb, "ref_bones", limb, "active_ref_bone")
		
		col = row.column()
		row = col.column(align=True)
		row.operator("pose.juar_ref_bone_add", icon="ZOOMIN", text="")
		row.operator("pose.juar_ref_bone_remove", icon="ZOOMOUT", text="")
			
		if len(limb.ref_bones) > 0:
			row = col.column(align=True)
			row.separator()
			row.operator("pose.juar_ref_bone_move", icon='TRIA_UP', text="").direction = 'UP'
			row.operator("pose.juar_ref_bone_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
			
		row = layout.row()
		if len(context.active_object.juar_limbs[context.active_object.juar_active_limb].ref_bones) > 0:
			col = row.column()
			row_ = col.column(align=True)
			row_.prop_search(limb.ref_bones[limb.active_ref_bone], "name", armature.data, "bones", text="Bone")
			col = row_.column()
			row_ = col.column(align=True)
			op = row.operator("pose.juar_limb_select_bone", icon="BONE_DATA", text="")
			op.bone = "active_ref_bone"
			
			row = layout.row()
			row.prop(limb.ref_bones[limb.active_ref_bone], "label")
			
class POSE_PT_juar_LiveAutoRefSpace(bpy.types.Panel):
	bl_label = "Live AutoRefSpace"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "AutoRefSpace"				
	
	@classmethod
	def poll(self, context):
		armature = context.active_object
		return armature and armature.type == "ARMATURE" and len(armature.juar_limbs) > 0 and context.mode == 'POSE'
		
	def draw(self, context):
		layout = self.layout
		armature = context.object
		limb = armature.juar_limbs[armature.juar_active_limb]
		
		#Check duplicates
		duplicate = False
		names = {}
		if limb.bone != "":
			names[limb.bone] = limb.bone
		for limb_ in armature.juar_limbs:
			if limb_.bone in names.keys() and limb_.id != limb.id:
				duplicate = True
				break
		del names
		
		
		row = layout.row()
		row.prop(limb, "active", toggle=True)
		#Do NOT let active for any of following cases : 
		#No bone
		if limb.bone == "":
			row.enabled = False
		#No reference
		if len(limb.ref_bones) == 0:
			row.enabled = False
		#Already generated
		if limb.generated == True:
			row.enabled = False
		#Duplicates
		if duplicate == True:
			row.enabled = False
			row = layout.row()
			row.label("Duplicate", icon='ERROR')
		#Bone can't be its own ref
		if limb.bone in [bone_.name for bone_ in limb.ref_bones] and limb.bone != "":
			row.enabled = False
			row = layout.row()
			row.label("Bone is its own ref", icon='ERROR')
		if (limb.active == False and limb.generated == False) and check_child_of_bone(limb.bone) == True:
			row.enabled = False
			row = layout.row()
			row.label("Already child of constraint on bone", icon='ERROR')			
		
		if limb.active == True:
			row = layout.row()
			row.prop(limb, "enum", text="Ref")
		
		if limb.generated == True:
			row = layout.row()
			row.operator("pose.juar_update_refspace", text="Update")
			
class POSE_PT_juar_LimbGenerate(bpy.types.Panel):
	bl_label = "Generate"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "AutoRefSpace"	
	
	@classmethod
	def poll(self, context):
		armature = context.active_object
		return armature and armature.type == "ARMATURE" and len(armature.juar_limbs) > 0 and context.mode == 'POSE'
		
	def draw(self, context):
		layout = self.layout
		armature = context.object
	
		#Check duplicates
		duplicate       = False
		some_empty_bone = False
		some_empty_refs = False
		own_ref         = False
		names = {}
		for limb_ in armature.juar_limbs:
			if limb_.bone in names.keys():
				duplicate = True
				break
			else:
				names[limb_.bone] = limb_.bone
			if limb_.bone == "":
				some_empty_bone = True
			if len(limb_.ref_bones) == 0:
				some_empty_refs = True
			if limb_.bone in [bone_.name for bone_ in limb_.ref_bones] and limb_.bone != "":
				own_ref = True
		del names

		row = layout.row()
		row.prop(armature.juar_generation, "view_location")
		row = layout.row()
		row.prop(armature.juar_generation, "panel_name")
		if armature.juar_generation.view_location == "TOOLS":
			row = layout.row()
			row.prop(armature.juar_generation, "tab_tool")
		row = layout.row()
		row.operator("pose.juar_generate_refspace", text="Generate")
		if duplicate == True or some_empty_bone == True or some_empty_refs == True or own_ref == True or check_child_of_list_bone([limb.bone for limb in armature.juar_limbs if (limb.generated == False and limb.active == False)]):
			row.enabled = False
		if duplicate == True:
			row = layout.row()
			row.label("Duplicate", icon='ERROR')
		if some_empty_bone == True:
			row = layout.row()
			row.label("Some bones are not filled", icon='ERROR')
		if some_empty_refs == True:
			row = layout.row()
			row.label("Some Refs are not filled", icon='ERROR')
		if check_child_of_list_bone([limb.bone for limb in armature.juar_limbs if (limb.generated == False and limb.active == False)]) == True:
			row = layout.row()
			row.label("Some bone have already child of constraint", icon='ERROR')			
		#Bone can't be its own ref
		if own_ref == True:
			row = layout.row()
			row.label("Some bones are self-ref", icon='ERROR')
		
class POSE_MT_JuAR_limb_specials(bpy.types.Menu):
	bl_label = "Limb Specials"

	def draw(self, context):
		layout = self.layout
	
		op = layout.operator("pose.juar_limb_copy", icon='COPY_ID', text="Copy Limb")
		op.mirror = False
		op = layout.operator("pose.juar_limb_copy", icon='ARROW_LEFTRIGHT', text="Mirror Copy Limb")
		op.mirror = True		
		
			
def register():
	bpy.utils.register_class(POSE_UL_juar_LimbList)
	bpy.utils.register_class(POSE_UL_juar_BoneList)
	bpy.utils.register_class(POSE_UL_JuAR_SideList)
	
	bpy.utils.register_class(POSE_PT_juar_AutoRefSpace_Limbs)
	bpy.utils.register_class(POSE_PT_juar_LimbDetail)
	bpy.utils.register_class(POSE_PT_juar_LiveAutoRefSpace)
	bpy.utils.register_class(POSE_PT_juar_LimbGenerate)
	
	bpy.utils.register_class(POSE_MT_JuAR_limb_specials)
	
def unregister():
	bpy.utils.unregister_class(POSE_UL_juar_LimbList)
	bpy.utils.unregister_class(POSE_UL_juar_BoneList)
	bpy.utils.unregister_class(POSE_UL_JuAR_SideList)
	
	bpy.utils.unregister_class(POSE_PT_juar_AutoRefSpace_Limbs)
	bpy.utils.unregister_class(POSE_PT_juar_LimbDetail)
	bpy.utils.unregister_class(POSE_PT_juar_LiveAutoRefSpace)
	bpy.utils.unregister_class(POSE_PT_juar_LimbGenerate)
	
	bpy.utils.register_class(POSE_MT_JuAR_limb_specials)
