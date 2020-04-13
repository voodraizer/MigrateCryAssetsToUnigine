import xml.etree.ElementTree as ET
import os
import shutil

from def_globals import *


def ImageMagicConvert(img, dest_path):
	'''

	'''

	converted_images = []

	from wand.image import Image
	from wand.color import Color

	filename, file_extension = os.path.splitext(os.path.basename(img))
	new_filename = ""
	base_filename = ""

	original = Image(filename = img)
	converted = original.convert('tga')
	
	# converted.format = 'tga'

	if (filename.endswith("_diff")):
		base_filename = filename[:-5]
		new_filename = base_filename + "_df"

	if (filename.endswith("_ddna")):
		base_filename = filename[:-5]
		new_filename = base_filename + "_nm"

		converted.alpha_channel = False
		# converted.alpha_channel = 'remove'

		gloss_img = original.clone()
		gloss_img.alpha_channel = 'extract'
		
		exported_file = os.path.join(dest_path, base_filename + "_gloss" + ".tga")
		converted_images.append(exported_file)
		
		gloss_img.save(filename = exported_file)
	
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

	exported_file = os.path.join(dest_path, new_filename + ".tga")
	converted_images.append(exported_file)

	converted.save(filename = exported_file)

	return converted_images



def ParseTexturesXmlList(xml_file):
	'''
	
	'''
	# print("XML file: " + xml_file)

	tree = ET.parse(xml_file)
	root = tree.getroot()

	#all_textures = root.iter('Texture')
	#textures_count = sum(1 for _ in all_textures)

	# for tex in all_textures:
	for tex in root.iter('Texture'):
		# parse textures
		path_xml = xml_get(tex, "path")
		path_orig = os.path.normpath(os.path.join(CRYENGINE_ASSETS_PATH, path_xml))
		path_rel = os.path.normpath(os.path.join(DESTINATION_ASSETS_PATH, os.path.dirname(path_xml)))

		print(path_orig + " == " + path_rel)

		#
		if not os.path.exists(path_rel):
			os.makedirs(path_rel)
		
		# imagemagic convert
		converted_images = ImageMagicConvert(path_orig, path_rel)

	pass


ParseTexturesXmlList(TEXTURES_XML)