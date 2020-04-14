import xml.etree.ElementTree as ET
import os
import shutil

from def_globals import *


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



def CreateUnigineXmlMaterial(cry_xml_root, unigine_mat_path):
	import uuid
	import hashlib

	mat_file_path = xml_get(cry_xml_root, "mtl_file")

	mat_name = xml_get(cry_xml_root, "name")
	mat_shader = xml_get(cry_xml_root, "shader")
	mat_gen_mask = xml_get(cry_xml_root, "gen_mask")

	# <?xml version="1.0" encoding="utf-8"?>

	xml_root = ET.Element('material')
	xml_root.set('version', "2.11.0.0")
	xml_root.set('name', mat_name)

	unigine_uuid = hashlib.sha1(unigine_mat_path.encode('utf-8'))
	xml_root.set('guid', unigine_uuid.hexdigest())
	# print("==================================================")
	# print(unigine_uuid.hexdigest())
	# print(unigine_mat_path)
	# print("==================================================")

	# material base type.
	if (mat_shader == "Illum"):
		xml_root.set('base_material', "mesh_base")
	# if (mat_shader == "Illum"):
	# 	xml_root.set('base_material', "decal_base")
	if (mat_shader == "Vegetation"):
		xml_root.set('base_material', "grass_base")


	# parse textures.
	for tex in cry_xml_root.iter('Texture'):
			tex_map = xml_get(tex, "map")
			tex_file = xml_get(tex, "file")

			# Convert texture path.
			rel_path = ''
			if (tex_file.startswith("./")):
				tex_file = tex_file[2:]
				rel_path = os.path.dirname(mat_file_path)
				rel_path = rel_path.replace('\\','/')
				# if (rel_path.startswith("models")):
				# 	rel_path = rel_path[7:]
				# if (rel_path.startswith("textures")):
				# 	rel_path = rel_path[9:]
			
			new_filename, aaaa = os.path.splitext(os.path.basename(tex_file))
			new_filename = convert_suffixes_to_unigine(new_filename)
			new_filename += ".tga"
			# print("==================================================")
			# print(new_filename)
			# print("==================================================")
				
			
			if (tex_map == "Diffuse"):
				xml_child = ET.SubElement(xml_root, 'texture')
				xml_child.text = os.path.join(rel_path, "Textures", new_filename)
				xml_child.set('name', "albedo")
			
			if (tex_map == "Bumpmap"):
				xml_child = ET.SubElement(xml_root, 'texture')
				xml_child.text = os.path.join(rel_path, "Textures", new_filename)
				xml_child.set('name', "normal")

			if (tex_map == "Opacity"):
				pass
			
			if (tex_map == "Detail"):
				pass

			if (tex_map == "Custom"):
				pass
			
			if (tex_map == "[1] Custom"):
				pass


	


	xml_child = ET.SubElement(xml_root, 'parameter')
	xml_child.text = "1"
	xml_child.set('name', "metalness")
	xml_child.set('expression', "0")


	xml_child = ET.SubElement(xml_root, 'parameter')
	xml_child.text = "1 1 1 1"
	xml_child.set('name', "specular_color")
	xml_child.set('expression', "0")


	xml_child = ET.SubElement(xml_root, 'parameter')
	xml_child.text = "1"
	xml_child.set('name', "gloss")
	xml_child.set('expression', "0")


	# print("==================================================")
	# print(xml_prettify(xml_root))
	# print("==================================================")
	
	return xml_root


def ParseMaterialsXmlList(xml_file):
	'''
	
	'''

	tree = ET.parse(xml_file)
	root = tree.getroot()

	for mat in root.iter('Material'):
		# print(' > name: ' + xml_get(mat, "name") + " shader: " + xml_get(mat, "shader"))

		if (xml_get(mat, "shader") == "Nodraw"):
			continue

		# put *.mat in materials subfolder
		cry_mat_file_path = xml_get(mat, "mtl_file")

		# path_orig = os.path.normpath(os.path.join(CRYENGINE_ASSETS_PATH, path_xml))
		path_rel = os.path.normpath(os.path.join(DESTINATION_ASSETS_PATH, os.path.dirname(cry_mat_file_path), "materials"))
		unigine_mat_path = os.path.join(path_rel, xml_get(mat, "name")) + ".mat"
		unigine_mat_path_rel = os.path.join(os.path.dirname(cry_mat_file_path), "materials") + "\\" + xml_get(mat, "name") + ".mat"

		# print("==================================================")
		# print(path_rel)
		# print(os.path.join(path_rel, xml_get(mat, "name")) + ".mat")
		# print("==================================================")

		# cry_mtl_obj = ParseCryMtlFile(os.path.join(root_dir, p))
		unigine_mat_xml = CreateUnigineXmlMaterial(mat, unigine_mat_path_rel)

		if not os.path.exists(path_rel):
			os.makedirs(path_rel)
		
		tree = ET.ElementTree(unigine_mat_xml)
		tree.write(unigine_mat_path)

	pass

ParseMaterialsXmlList(MATERIALS_XML)
# CreateUnigineXmlMaterial("")