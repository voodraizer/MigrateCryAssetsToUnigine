import xml.etree.ElementTree as ET
import os

from def_globals import *



def Create_models_xml_list(root_dir):
	'''
	Create xml list from all models (fbx).
	'''
	# listOfFile = os.listdir(root_dir)
	# for entry in listOfFile:
	# 	if os.path.isdir(os.path.join(root_dir, entry)): print("Folder: ", entry)
	# 	if os.path.isfile(os.path.join(root_dir, entry)): print("File: ", entry)
	# 	# print(entry)
	
	
	xml_root = ET.Element('Models')

	full_file_paths = get_filepaths(root_dir, "model")
	for p in full_file_paths:
		child = ET.SubElement(xml_root, 'Model', {'path':p})

		# Get cryasset for model.
		cryasset = os.path.join(root_dir, p.replace(".fbx", ".cgf.cryasset"))
		if (not os.path.exists(cryasset)):
			logging.error("Cryasset not found.\n\t\t" + cryasset)
			continue
		
		cryasset_tree = ET.parse(cryasset)
		dependencies_root = cryasset_tree.getroot().find(".//Dependencies")
		for path in dependencies_root:
			child.set("mtl_path", path.text)


	# print(xml_prettify(xml_top))
	tree = ET.ElementTree(xml_root)
	tree.write(MODELS_XML)



def Create_materials_xml_list(root_dir):
	'''
	Create xml list from materials (mtl).
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
	'''
	Create xml list from textures (tif).
	'''

	xml_root = ET.Element('Textures')

	full_file_paths = get_filepaths(root_dir, "image")
	for p in full_file_paths:
		
		import re
		path = p.lower()
		re.split('. |\\|/', path)
		
		# Collect only tif files in models and textures folders.
		if (".dds" in path): continue
		if ((not "models" in path) and (not "textures" in path)): continue

		child = ET.SubElement(xml_root, 'Texture', {'path':p})

	# print(xml_prettify(xml_top))
	tree = ET.ElementTree(xml_root)
	tree.write(TEXTURES_XML)

	pass


def Create_prefabs_xml_list(root_dir):
	'''
	Create xml list from prefabs.
	'''

	pass


def Create_levels_xml_list(root_dir):
	'''
	Create xml list from levels.
	'''

	pass


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

			# Check if texture not exist or dds.
			filename, file_extension = os.path.splitext(cry_texture["file"])
			if (file_extension == ".dds"):
				cry_texture["file"] = filename + ".tif"
			
			full_texture_path = os.path.join(CRYENGINE_ASSETS_PATH, cry_texture["file"])

			if (cry_texture["file"].startswith("./")):
				# path relative to current folder
				full_texture_path = os.path.join(CRYENGINE_ASSETS_PATH, os.path.dirname(cry_mtl_obj["mtl_file"]), cry_texture["file"][2:])
				full_texture_path = full_texture_path.replace('\\','/')
			else:
				# try search texture.
				# rel_path = Searach_texture(CRYENGINE_ASSETS_PATH, cry_texture["file"])
				# full_texture_path = os.path.join(CRYENGINE_ASSETS_PATH, rel_path).replace('\\','/')
				pass
			
			if (not os.path.exists(full_texture_path)):
				logging.error("\nMaterial texture missing: " + cry_texture["file"] + "\n" + full_texture_path)

			#
			cry_material["textures"].append(cry_texture)
		
		# fix
		# if (cry_material["name"] == None): cry_material["name"] = os.path.splitext(os.path.basename(xml_file))[0]
	
		cry_mtl_obj["materials"].append(cry_material)
	
	return cry_mtl_obj


def ParseModels(xml_file):
	'''
	
	'''
	tree = ET.parse(xml_file)
	root = tree.getroot()

	for model in root:
		# parse models
		# print(model.tag, model.attrib)
		print(model.get("name"), " ", model.get("type"), " ", model.get("path"))
		for mat in model.iter('Material'):
			# parse materials
			print("		", mat.get("name"), " ", mat.get("path"))
