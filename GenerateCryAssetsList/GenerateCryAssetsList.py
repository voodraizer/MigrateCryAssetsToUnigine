import xml.etree.ElementTree as ET
import os

# CRYENGINE_ASSETS_PATH = "c:/_CRYENGINE_BUILDS/0AZ/Assets/"
CRYENGINE_ASSETS_PATH = "c:/_CRYENGINE_BUILDS/0AZ_test/Assets/"
UE_ASSETS_PATH = ""

MODELS_XML = 'd:/Downloads/PyQt/models_list.xml'
MATERIALS_XML = 'd:/Downloads/PyQt/materials_list.xml'
TEXTURES_XML = 'd:/Downloads/PyQt/textures_list.xml'


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

def Create_models_xml_list(root_dir):
	# listOfFile = os.listdir(root_dir)
	# for entry in listOfFile:
	# 	if os.path.isdir(os.path.join(root_dir, entry)): print("Folder: ", entry)
	# 	if os.path.isfile(os.path.join(root_dir, entry)): print("File: ", entry)
	# 	# print(entry)
	
	full_file_paths = get_filepaths(root_dir, "image")
	for p in full_file_paths:
		print(" > ", p)

	pass


def Create_materials_xml_list(root_dir):
	'''
	Create xml list from materials.
	'''

	xml_root = ET.Element('Materials')

	full_file_paths = get_filepaths(root_dir, "material")

	for p in full_file_paths:
		cry_mtl_obj = ParseCryMtlFile(os.path.join(root_dir, p))
		
		for mat in cry_mtl_obj["materials"]:
			mat_child = ET.SubElement(xml_root, 'Material')
			mat_child.set('mtl_file', cry_mtl_obj.get("mtl_file")[len(root_dir):])
			mat_child.set('name', mat.get("name"))
			mat_child.set('shader', mat.get("shader"))
			mat_child.set('gen_mask', mat.get("gen_mask"))
			mat_child.set('string_gen_mask', mat.get("string_gen_mask"))
			mat_child.set('surface_type', mat.get("surface_type"))
			mat_child.set('diffuse', mat.get("diffuse"))
			mat_child.set('specular', mat.get("specular"))
			mat_child.set('opacity', mat.get("opacity"))
			mat_child.set('shininess', mat.get("shininess"))
			mat_child.set('alpha_test', mat.get("alpha_test"))
			mat_child.set('emissive', mat.get("emissive"))

			for tex in mat["textures"]:
				tex_child = ET.SubElement(mat_child, 'Texture')
				tex_child.set('map', tex.get("map"))
				tex_child.set('file', tex.get("file"))

	# print(xml_prettify(xml_top))
	tree = ET.ElementTree(xml_root)
	tree.write(MATERIALS_XML)

	pass


def Create_textures_xml_list(root_dir):
	xml_root = ET.Element('Textures')

	full_file_paths = get_filepaths(root_dir, "image")
	for p in full_file_paths:
		child = ET.SubElement(xml_root, 'Texture', {'path':p})

	# print(xml_prettify(xml_top))
	tree = ET.ElementTree(xml_root)
	tree.write(TEXTURES_XML)

	pass


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
				pass


	return file_paths


def ParseCryMtlFile(xml_file):
	'''
	Parsing cry mtl file.
	return {object}
	'''

	tree = ET.parse(xml_file)
	root = tree.getroot()

	cry_mtl_obj = {}
	cry_mtl_obj["mtl_file"] = xml_file
	cry_mtl_obj["materials"] = []

	submat_root = root

	if (root.find('SubMaterials') != None): submat_root = root.find('SubMaterials')


	for mat in submat_root.iter('Material'):
		# parse materials
		cry_material = {}
		cry_material["name"] = xml_get(mat, "Name")
		cry_material["shader"] = xml_get(mat, "Shader")
		cry_material["gen_mask"] = xml_get(mat, "GenMask")
		cry_material["string_gen_mask"] = xml_get(mat, "StringGenMask")
		cry_material["surface_type"] = xml_get(mat, "SurfaceType")
		cry_material["diffuse"] = xml_get(mat, "Diffuse")
		cry_material["specular"] = xml_get(mat, "Specular")
		cry_material["opacity"] = xml_get(mat, "Opacity")
		cry_material["shininess"] = xml_get(mat, "Shininess")
		cry_material["alpha_test"] = xml_get(mat, "AlphaTest")
		cry_material["emissive"] = xml_get(mat, "Emissive")

		cry_material["textures"] = []

		for tex in mat.iter('Texture'):
			# parse textures.
			cry_texture = {}
			cry_texture["map"] = xml_get(tex, "Map")
			cry_texture["file"] = xml_get(tex, "File")

			cry_material["textures"].append(cry_texture)
		
		# fix
		# if (cry_material["name"] == None): cry_material["name"] = os.path.splitext(os.path.basename(xml_file))[0]
	
		cry_mtl_obj["materials"].append(cry_material)
	
	return cry_mtl_obj

def ParseModels(xml_file):
	tree = ET.parse(xml_file)
	root = tree.getroot()

	for model in root:
		# parse models
		# print(model.tag, model.attrib)
		print(model.get("name"), " ", model.get("type"), " ", model.get("path"))
		for mat in model.iter('Material'):
			# parse materials
			print("		", mat.get("name"), " ", mat.get("path"))

def ParseMaterials(xml_file):

	pass

def ParseTextures(xml_file):

	pass


# ParseModels(MODELS_XML)
# Create_models_xml_list(CRYENGINE_ASSETS_PATH)
Create_textures_xml_list(CRYENGINE_ASSETS_PATH)
Create_materials_xml_list(CRYENGINE_ASSETS_PATH)