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
			logging.error("\n\t\t\tCryasset not found.\n\t\t\t" + cryasset)
			continue
		
		cryasset_tree = ET.parse(cryasset)
		dependencies_root = cryasset_tree.getroot().find(".//Dependencies")
		for path in dependencies_root:
			child.set("mtl_path", path.text)


	# print(xml_prettify(xml_top))
	tree = ET.ElementTree(xml_root)
	tree.write(MODELS_XML)


def Validate_materals_xml_paths():
	'''

	'''
	logging.info("\n\t\t\tStart validating texture paths in materials\n\n")

	tree = ET.parse(MATERIALS_XML)
	root = tree.getroot()

	error_count = 0

	for mat in root.iter('Material'):
		# parse materials
		# xml_get(mat, "Name")

		for tex in mat.iter('Texture'):
			# parse textures.
			# xml_get(tex, "map")
			rel_path = xml_get(tex, "file")
			rel_path_orig = xml_get(tex, "file_orig")
			full_path = os.path.join(CRYENGINE_ASSETS_PATH, rel_path)
			if (rel_path == "" or not os.path.exists(full_path)):
				logging.error("\n\t\t\tMaterial texture missing: " + rel_path + "\n\t\t\t" + full_path + "\n\t\t\t" + rel_path_orig)
				error_count += 1
	
	logging.info("\n\n\t\t\tEnd validating.\n\t\t\t" + "Errors: " + str(error_count) + "\n\n")

	pass


def Create_materials_xml_list(root_dir):
	'''
	Create xml list from materials (mtl).
	'''

	all_textures = get_filepaths(CRYENGINE_ASSETS_PATH, "image")


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
				tex_child.set('file_orig', tex.get("file"))

				# make path valid.
				orig_tex_path = tex.get("file").replace(".dds", ".tif")
				# tex_child.set('file', tex.get("file"))
				mat_file_dir = os.path.dirname(cry_mtl_obj.get("mtl_file"))
				
				if (orig_tex_path.startswith("./")):
					# path relative to current folder
					search_path = os.path.normpath(os.path.join(mat_file_dir, os.path.dirname(orig_tex_path), os.path.basename(orig_tex_path)))
					if (not os.path.exists(search_path)):
						# print("Path not: " + search_path)
						# Search_texture_file(all_textures, search_path)
						tex_child.set('file', "")
					else:
						tex_child.set('file', search_path[len(CRYENGINE_ASSETS_PATH):])
					pass
					
				if (orig_tex_path.lower().startswith("models")):
					# path relative to models
					search_path = os.path.normpath(os.path.join(CRYENGINE_ASSETS_PATH, os.path.dirname(orig_tex_path), os.path.basename(orig_tex_path)))
					if (not os.path.exists(search_path)):
						# print("Path not: " + search_path)
						tex_child.set('file', "")
					else:
						tex_child.set('file', search_path[len(CRYENGINE_ASSETS_PATH):])
					pass
					
				if (orig_tex_path.lower().startswith("textures")):
					# path relative to textures
					search_path = os.path.normpath(os.path.join(CRYENGINE_ASSETS_PATH, os.path.dirname(orig_tex_path), os.path.basename(orig_tex_path)))
					if (not os.path.exists(search_path)):
						# print("Path not: " + search_path)
						tex_child.set('file', "")
					else:
						tex_child.set('file', search_path[len(CRYENGINE_ASSETS_PATH):])
					pass

				if (orig_tex_path.lower().startswith("objects")):
					search_path = os.path.normpath(os.path.join(CRYENGINE_ASSETS_PATH, os.path.dirname(orig_tex_path), os.path.basename(orig_tex_path)))
					if (not os.path.exists(search_path)):
						# print("Path not: " + search_path)
						tex_child.set('file', "")
					else:
						tex_child.set('file', search_path[len(CRYENGINE_ASSETS_PATH):])
					pass
				

	# print(xml_prettify(xml_top))

	tree = ET.ElementTree(xml_root)
	tree.write(MATERIALS_XML)

	# Validate textures path in materials xml.
	Validate_materals_xml_paths()

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
