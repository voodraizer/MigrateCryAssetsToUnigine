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



def CreateUnigineXmlMaterial(cry_xml_root):

	mat_name = xml_get(cry_xml_root, "name")
	mat_shader = xml_get(cry_xml_root, "shader")
	mat_gen_mask = xml_get(cry_xml_root, "gen_mask")

	# print("==================================================")
	# print(mat_name)
	# print(mat_shader)
	# print(mat_gen_mask)
	# print("==================================================")


	# <?xml version="1.0" encoding="utf-8"?>

	xml_root = ET.Element('material')
	xml_root.set('version', "2.11.0.0")
	xml_root.set('name', mat_name)
	xml_root.set('guid', "909d862e726317b5d7964590d9d7dbafc203d542")

	if (mat_shader == "Illum"):
		xml_root.set('base_material', "mesh_base")
	# if (mat_shader == "Illum"):
	# 	xml_root.set('base_material', "decal_base")
	if (mat_shader == "Vegetation"):
		xml_root.set('base_material', "grass_base")


	# xml_child = ET.SubElement(xml_root, 'texture')
	# xml_child.text = "D:/path to albedo"
	# xml_child.set('name', "albedo")


	# xml_child = ET.SubElement(xml_root, 'parameter')
	# xml_child.text = "1"
	# xml_child.set('name', "metalness")
	# xml_child.set('expression', "0")


	# xml_child = ET.SubElement(xml_root, 'parameter')
	# xml_child.text = "1 1 1 1"
	# xml_child.set('name', "specular_color")
	# xml_child.set('expression', "0")


	# xml_child = ET.SubElement(xml_root, 'parameter')
	# xml_child.text = "1"
	# xml_child.set('name', "gloss")
	# xml_child.set('expression', "0")


	print("==================================================")
	print(xml_prettify(xml_root))
	print("==================================================")
	
	pass


def ParseMaterialsXmlList(xml_file):
	'''
	
	'''

	tree = ET.parse(xml_file)
	root = tree.getroot()

	for mat in root.iter('Material'):
		# print(' > name: ' + xml_get(mat, "name") + " shader: " + xml_get(mat, "shader"))

		if (xml_get(mat, "shader") == "Nodraw"):
			continue

		# cry_mtl_obj = ParseCryMtlFile(os.path.join(root_dir, p))
		CreateUnigineXmlMaterial(mat)

		for tex in mat.iter('Texture'):
			# print(' 	> map: ' + xml_get(tex, "map") + " file: " + xml_get(tex, "file"))
			pass

		pass

		# put *.mat in materials subfolder

	pass

ParseMaterialsXmlList(MATERIALS_XML)
# CreateUnigineXmlMaterial("")