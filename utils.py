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

#shortcut to prefs
def addonpref():
	user_preferences = bpy.context.user_preferences
	return user_preferences.addons[__package__].preferences

def get_name(bone):
	return bone
	
def get_symm_name(bone):
	#first check if last digit are .xxx with [dot] and then xxx is integer
	end_name = ""
	if bone[len(bone)-4:len(bone)-3] == '.' and bone[len(bone)-3:].isdigit():
		end_pos = len(bone) - 4
		end_name = bone[len(bone)-4:]
	else:
		end_pos = len(bone)
		
		
	#construct dict for each length of potential side
	side_len = {}
	for side in addonpref().sides:
		if len(side.name_R) in side_len.keys():
			side_len[len(side.name_R)].append((side.name_R, side.name_L))
		else:
			side_len[len(side.name_R)] = []
			side_len[len(side.name_R)].append((side.name_R, side.name_L))
		if len(side.name_L) in side_len.keys():
			side_len[len(side.name_L)].append((side.name_L, side.name_R))
		else:
			side_len[len(side.name_L)] = []
			side_len[len(side.name_L)].append((side.name_L, side.name_R))
			
	for side_l in side_len.keys():
		if bone[end_pos-side_l:end_pos] in [name[0] for name in side_len[side_l]]:
			return bone[:end_pos-side_l] + side_len[side_l][[name[0] for name in side_len[side_l]].index(bone[end_pos-side_l:end_pos])][1] + end_name
	return bone


def init_sides(context):
	sides = addonpref().sides
	side = sides.add()
	side.name_R = ".R"
	side.name_L = ".L"
	side = sides.add()
	side.name_R = ".r"
	side.name_L = ".l"
	side = sides.add()
	side.name_R = "right"
	side.name_L = "left"
	addonpref().active_side = 2
	
def check_child_of_list_bone(bones):
	for bone in bones:
		if check_child_of_bone(bone) == True:
			return True
	return False
			
def check_child_of_bone(bone):
	if bone != "":
		for constr in bpy.context.object.pose.bones[bone].constraints:
			if constr.type == "CHILD_OF":
				return True
	return False
			
def set_active(bone_name):
	armature = bpy.context.object
	bpy.ops.pose.select_all(action='DESELECT')
	armature.data.bones[bone_name].select = True
	armature.data.bones.active = armature.data.bones[bone_name]
	
def global_checks():
	armature = bpy.context.object
	
	duplicate       = False
	some_empty_bone = False
	some_empty_refs = False
	some_own_ref    = False
	some_constraint = False
	
	names = {}
	for limb_ in armature.juar_limbs:
		if limb_.bone in names.keys():
				duplicate = True
				break
		else:
			names[limb_.bone] = limb_.bone

		empty_bone, empty_refs, own_ref, constraint = checks(limb_)
		if some_empty_bone == False:
			some_empty_bone = empty_bone
		if some_empty_refs == False:
			some_empty_bone = empty_refs
		if some_own_ref == False:
			some_own_ref = own_ref
		if some_constraint == False:
			some_constraint = constraint
	del names
	
	return duplicate, some_empty_bone, some_empty_refs, some_own_ref, some_constraint
		
def checks(limb_):
	
	empty_bone  = False
	empty_refs  = False
	own_ref     = False
	constraint  = False
	
	if limb_.bone == "":
		empty_bone = True
	if len(limb_.ref_bones) == 0:
		empty_refs = True
	if limb_.bone in [bone_.name for bone_ in limb_.ref_bones] and limb_.bone != "":
		own_ref = True	
	if (limb_.active == False and limb_.generated == False) and check_child_of_bone(limb_.bone):
		constraint = True
		
	return empty_bone, empty_refs, own_ref, constraint
	
def check_single_duplicate(single_limb):
	armature = bpy.context.object
	
	duplicate = False
	
	names = {}
	for limb_ in armature.juar_limbs:
		if limb_.bone != single_limb.bone:
			continue
		if limb_.bone in names.keys():
				duplicate = True
				break
		else:
			names[limb_.bone] = limb_.bone
	del names
	
	return duplicate
