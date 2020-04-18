
import os
import logging

# Engines assets.
CRYENGINE_ASSETS_PATH = "d:/CRY_MIGRATE/Assets/" ### "d:/___TMP_CRY_ASSETS/Assets/"
TMP_EXPORT_ASSETS_PATH = "D:/___TMP_UNIGINE_EXPORT/"
DESTINATION_ASSETS_PATH = "d:/UNIGINE Projects/UNIGINE_MIGRATE_FROM_CRY/data/" ### "d:/UNIGINE Projects/Test_1/data/"

# Exported xml.
MODELS_XML = TMP_EXPORT_ASSETS_PATH + 'models_list.xml'
MATERIALS_XML = TMP_EXPORT_ASSETS_PATH + 'materials_list.xml'
TEXTURES_XML = TMP_EXPORT_ASSETS_PATH + 'textures_list.xml'
PREFABS_XML = TMP_EXPORT_ASSETS_PATH + 'prefabs_list.xml'
LEVELS_XML = TMP_EXPORT_ASSETS_PATH + 'levels_list.xml'

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

# DEBUG
DEBUG_DISABLE_IMAGE_CONV = True



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
			if (type == "image" and (filename.endswith(".tif") or filename.endswith(".dds"))):
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
		base_filename = filename[:-5]
		new_filename = base_filename + "_s"

	if (filename.endswith("_mask")):
		base_filename = filename[:-5]
		new_filename = base_filename + "_mask"
	
	if (filename.endswith("_detail")):
		base_filename = filename[:-7]
		new_filename = base_filename + "_detail"
		pass
	
	if (filename.endswith("_sss")):
		base_filename = filename[:-4]
		new_filename = base_filename + "_sss"

	if (filename.endswith("_displ")):
		base_filename = filename[:-6]
		new_filename = base_filename + "_h"

	return new_filename


def Mtl_texture_path_to_relative_unigine(tex_file, mat_file_path):
	'''

	'''

	# Convert texture path.
	new_filename, new_ext = os.path.splitext(os.path.basename(tex_file))
	new_filename = convert_suffixes_to_unigine(new_filename)
	new_filename += ".tga"

	rel_path = ''

	if (tex_file.startswith("./")):
		# path relative to current folder
		rel_path = os.path.join(os.path.dirname(mat_file_path), os.path.dirname(tex_file[2:]), new_filename)
		rel_path = rel_path.replace('\\','/')
		
	if (tex_file.lower().startswith("models")):
		# path relative to models
		rel_path = os.path.join(os.path.dirname(mat_file_path), "Textures", new_filename).replace('\\','/')
		pass
	if (tex_file.lower().startswith("textures")):
		# path relative to textures
		rel_path = (os.path.dirname(tex_file) + "/" + new_filename).replace('\\','/')
	
	return rel_path

def Mtl_texture_path_to_relative(tex_file, mat_file_path):
	'''

	'''

	# Convert texture path.
	file_name, file_ext = os.path.splitext(os.path.basename(tex_file))

	rel_path = ''
		
	if (tex_file.startswith("./")):
		# path relative to current folder
		rel_path = os.path.join(os.path.dirname(mat_file_path), os.path.dirname(tex_file[2:]), file_name) + file_ext
		
	if (tex_file.lower().startswith("models")):
		# path relative to models
		rel_path = os.path.join(os.path.dirname(mat_file_path), "Textures", file_name).replace('\\','/') + file_ext
		
	if (tex_file.lower().startswith("textures")):
		# path relative to textures
		rel_path = (os.path.dirname(tex_file) + "/" + file_name).replace('\\','/') + file_ext

	if (tex_file.lower().startswith("objects")):
		# path relative to objects
		rel_path = tex_file
	
	rel_path = rel_path.replace('\\','/')

	if (rel_path == ""): logging.error("\nWrong path convert: " + tex_file + "\nResult: " + rel_path)

	return rel_path


def Search_texture_file(ALL_TEXTURES, full_path):
	'''
	1. search original tif file from full_path.
	2. search the same dds.
	3. search along all texture files in project.
	'''

	file_name, file_ext = os.path.splitext(os.path.basename(full_path.lower()))

	found_files = []

	for p in ALL_TEXTURES:
		f, e = os.path.splitext(os.path.basename(p.lower()))
		if (file_name == f): found_files.append(p)
	
	for p in found_files:
		f, e = os.path.splitext(os.path.basename(p.lower()))
		if (e == ".tif"): return os.path.normpath(os.path.join(CRYENGINE_ASSETS_PATH, p))
	
	for p in found_files:
		f, e = os.path.splitext(os.path.basename(p.lower()))
		if (e == ".dds"): return os.path.normpath(os.path.join(CRYENGINE_ASSETS_PATH, p))

	logging.error("\nTexture not found (tif and dds): " + full_path)

	return ""


def Search_texture_file_by_name(exported_textures, full_path):
	'''
	TODO: check texture mode, size for more preсise search ???
	'''

	file_name, file_ext = os.path.splitext(os.path.basename(os.path.normpath(full_path.lower())))
	
	for f_path in exported_textures:

		f_name, f_ext = os.path.splitext(os.path.basename(os.path.normpath(f_path.lower())))
		if (file_name == f_name):
			# print("\n\n" + file_name + " already exported.\n")
			return True

	return False

def Searach_texture(root_path, tex_file):
	rel_path = ""

	file_name, file_ext = os.path.splitext(os.path.basename(tex_file))

	# if (tex_file.startswith("../") or tex_file.startswith("..\\")):
	# print("\nTRY: " + tex_file)
	all_textures = get_filepaths(root_path, "image")
	
	found_files = []
	for tex in all_textures:
		f, e = os.path.splitext(os.path.basename(tex.lower()))
		if (file_name == f): found_files.append(tex)
	
	for p in found_files:
		if ((not "defaults" in p) and (not "generic" in p) and (not "natural" in p)): # try exclude some cryengine default folders
			rel_path = p.replace(root_path, "")
			# print("\nREL PATH: " + rel_path + "\n")
			break
	
	if (rel_path == ""):
		for p in found_files:
			rel_path = p.replace(root_path, "")
			# print("\nREL PATH: " + rel_path + "\n")
			break
	
	return rel_path

