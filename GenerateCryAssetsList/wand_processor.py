
# import xml.etree.ElementTree as ET
import os
# import shutil

from wand.image import Image
from wand.color import Color


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
		# albedo (RGB, RGB+A)
		base_filename = filename[:-5]
		new_filename = base_filename + "_alb"

	if (filename.endswith("_ddna")):
		# normalmap (RG)
		base_filename = filename[:-5]
		new_filename = base_filename + "_n"

		converted.alpha_channel = False
		# converted.alpha_channel = 'remove'

		gloss_img = original.clone()
		gloss_img.alpha_channel = 'extract'
		
		# shading (R-metalness, G-roughness, B-specular)
		exported_file = os.path.join(dest_path, base_filename + "_sh" + ".tga")
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

	# print(new_filename + ".tga")
	# print(exported_file)

	converted.save(filename = exported_file)

	return converted_images


def ImageMagicConvertBySet(imgs, dest_path):
	'''

	'''
	converted_images = []

	for img in imgs:

		filename, file_extension = os.path.splitext(os.path.basename(img))
		new_filename = ""
		base_filename = ""

		original = Image(filename = img)
		converted = original.convert('tga')
		
		# converted.format = 'tga'

		if (filename.endswith("_diff")):
			# unigine albedo (RGB, RGB+A)
			base_filename = filename[:-5]
			new_filename = base_filename + "_alb"

		if (filename.endswith("_ddna")):
			# unigine normalmap (RG)
			base_filename = filename[:-5]
			new_filename = base_filename + "_n"

			converted.alpha_channel = False
			# converted.alpha_channel = 'remove'

			# unigine shading (R-metalness, G-roughness, B-specular)
			# extract cryengine gloss (A) to G and invert
			gloss_img = original.clone()
			gloss_img.alpha_channel = 'extract'
			
			exported_file = os.path.join(dest_path, base_filename + "_sh" + ".tga")
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

		# print(new_filename + ".tga")
		# print(exported_file)

		converted.save(filename = exported_file)
	

	return converted_images
