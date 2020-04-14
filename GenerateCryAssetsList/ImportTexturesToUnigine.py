import xml.etree.ElementTree as ET
import os
import shutil

from def_globals import *
from wand_processor import *



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

		if (not os.path.exists(path_orig)):
			# print("====================================================")
			# print("File not exists: " + path_orig)
			# print("====================================================")
			continue

		#print(path_orig + " == " + path_rel)

		#
		if not os.path.exists(path_rel):
			os.makedirs(path_rel)
		
		# imagemagic convert
		converted_images = ImageMagicConvert(path_orig, path_rel)

	pass


ParseTexturesXmlList(TEXTURES_XML)