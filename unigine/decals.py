import sys
import os
import logging

path = os.path.dirname(os.path.abspath(__file__))[:-7]
sys.path.append(path)
import def_globals

from utils import *

decals_dir = def_globals.DESTINATION_ASSETS_PATH + "materials/decals"


#   <?xml version="1.0" encoding="utf-8" ?>
#  <material version="2.11.0.0" name="puddle" guid="7c71d0d6e63b73be36a98fd3f085fba2dc8d925e" parent="add324aa86356d87a7da66773fd79331801d0bd6" base_material="decal_base">
#   <blend src="src_alpha" dest="one_minus_src_alpha" />
#   <state name="parallax">1</state>
#   <texture name="albedo">guid://83a8df5776426c2d6dcf61db41898fbcf2c78d7a</texture>
#   <texture name="normal">guid://c9d71497997a4d79f6bc070112cad4a7f2589e2d</texture>
#   <texture name="shading">guid://3795851fe9a5cb3508e6c21f799d0dbb650fab8b</texture>
#   <texture name="parallax">guid://eb7ac66d5594f485eb1993dd3dd136a06aa7efe5</texture>
#   <parameter name="material_mask" expression="0">16777215</parameter>
#   <parameter name="angle_fade_threshold" expression="0">-1</parameter>
#   <parameter name="angle_fade_pow" expression="0">2</parameter>
#   <parameter name="parallax_scale" expression="0">0.00999999978</parameter>
#   </material>

def CreatedecalMaterial(mat_path, mat_name, textures = []):
	import uuid
	import hashlib
	import xml.etree.ElementTree as ET

	mat_path = def_globals.DESTINATION_ASSETS_PATH + "materials/decals/" + mat_path + "/" + mat_name + ".mat"

	rel_dir = mat_path[len(def_globals.DESTINATION_ASSETS_PATH):]
	rel_path = rel_dir + "/" + mat_name + ".mat"

	root = ET.Element('material')
	root.set("version", "2.11.0.0")
	root.set("name", mat_name)
	root.set("guid", hashlib.sha1(rel_path.encode('utf-8')).hexdigest())
	root.set("base_material", "decal_base")

	child = ET.SubElement(root, 'blend')
	child.set("src", "src_alpha")
	child.set("dest", "one_minus_src_alpha")

	for t in textures:
		child = ET.SubElement(root, 'texture')
		if ("_alb.tga" in t): child.set("name", "albedo")
		if ("_sh.tga" in t): child.set("name", "shading")
		if ("_n.tga" in t): child.set("name", "normal")
		if ("_h.tga" in t): child.set("name", "parallax")
		child.text = "Textures\\Decals\\" + t
		pass

	# child = ET.SubElement(root, 'parameter')

	indent(root)
	tree = ET.ElementTree(root)

	if (not os.path.exists(os.path.dirname(mat_path))): os.makedirs(os.path.dirname(mat_path))
	tree.write(mat_path)

	print("==================================================")
	# print(mat_path)
	# ET.dump(root)
	print("==================================================")

	pass

def CreateDecalMaterials():

	directory = def_globals.DESTINATION_ASSETS_PATH + "Textures/Decals/"

	files = get_filepaths(directory, "tga")
	for f in files:
		if (not f.endswith("_alb.tga")): continue

		textures = []

		basedir = os.path.dirname(f)
		basename = os.path.basename(f)
		basename = basename.replace("_alb.tga", "")

		decl_files = get_filepaths(directory + "\\" + basedir, "tga")
		for d_f in decl_files:
			if (os.path.basename(d_f).startswith(basename)):
				textures.append(basedir + d_f)

		# print(list(textures))
		print(basedir)

		# CreatedecalMaterial(directory + basedir, basename, textures)
		CreatedecalMaterial(basedir, basename, textures)

	pass


# =============================================================================
#
# =============================================================================
if __name__ == "__main__":

	CreateDecalMaterials()
	pass