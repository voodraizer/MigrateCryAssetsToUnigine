
import os
import logging

# Engines assets.
CRYENGINE_ASSETS_PATH = "d:/___TMP_CRY_ASSETS/Assets/"		### "c:/GITs/GameSDK/Assets/Assets/"
TMP_EXPORT_ASSETS_PATH = "D:/___TMP_UNIGINE_EXPORT/"
DESTINATION_ASSETS_PATH = "d:/UNIGINE Projects/Test_1/data/"

# Exported xml.
MODELS_XML = TMP_EXPORT_ASSETS_PATH + 'models_list.xml'
MATERIALS_XML = TMP_EXPORT_ASSETS_PATH + 'materials_list.xml'
TEXTURES_XML = TMP_EXPORT_ASSETS_PATH + 'textures_list.xml'
PREFABS_XML = TMP_EXPORT_ASSETS_PATH + 'prefabs_list.xml'
LEVELS_XML = TMP_EXPORT_ASSETS_PATH + 'levels_list.xml'
#TEXTURES_CONV_TMP = 'd:/Downloads/PyQt/TMP/'

# Base materials.
# MG_GENERAL = "/Game/Materials/General/MG_General"
# MG_TREES = "/Game/Materials/General/MG_Trees"
# MG_GRASS = "/Game/Materials/General/MG_Grass"
# MG_DECAL = "/Game/Materials/General/MG_Decal"
# MG_GLASS = "/Game/Materials/General/MG_Glass"

# Prefixes.
# PR_MI_MAT = "MI_"
# PR_MAT = "M_"
# PR_PREFAB = "PRF_"

# Logger.
LOG_EXPORTFROM_FILE = TMP_EXPORT_ASSETS_PATH + "export_from_log.txt"
LOG_EXPORTTO_FILE = TMP_EXPORT_ASSETS_PATH + "export_to_log.txt"





# =============================================================================
# 
# =============================================================================
def xml_prettify(elem):
	"""
	Return a pretty-printed XML string for the Element.
	"""

	from xml.etree import ElementTree
	from xml.dom import minidom

	rough_string = ElementTree.tostring(elem, 'utf-8')
	reparsed = minidom.parseString(rough_string)
	return reparsed.toprettyxml(indent="  ")


def xml_get(node, attr):
	'''
	Get attribute from xml node.
	Return value or ''.
	'''

	res = node.get(attr)

	if (res == None): return ""
	return res


def get_filepaths(directory, type):
	"""
	Generate the file names in a directory 
	tree by walking the tree either top-down or bottom-up. For each 
	directory in the tree rooted at directory top (including top itself), 
	it yields a 3-tuple (dirpath, dirnames, filenames).
	"""
	file_paths = []  # List which will store all of the full filepaths.

	# Walk the tree.
	for root, directories, files in os.walk(directory):
		for filename in files:
			if (type == "image" and filename.endswith(".tif")):
				filepath = os.path.join(root, filename)
				filepath = filepath[len(directory):]
				file_paths.append(filepath)

			if (type == "material" and filename.endswith(".mtl")):
				filepath = os.path.join(root, filename)
				filepath = filepath[len(directory):]
				file_paths.append(filepath)
			
			if (type == "model" and filename.endswith(".fbx")):
				filepath = os.path.join(root, filename)
				filepath = filepath[len(directory):]
				file_paths.append(filepath)


	return file_paths


def convert_suffixes_to_unigine(filename):
	new_filename = ""

	if (filename.endswith("_diff")):
		base_filename = filename[:-5]
		new_filename = base_filename + "_alb"

	if (filename.endswith("_ddna")):
		base_filename = filename[:-5]
		new_filename = base_filename + "_n"
	
	if (filename.endswith("_spec")):
		pass
	
	if (filename.endswith("_sss")):
		pass

	if (filename.endswith("_mask")):
		pass
	
	if (filename.endswith("_detail")):
		pass

	if (filename.endswith("_displ")):
		pass

	return new_filename