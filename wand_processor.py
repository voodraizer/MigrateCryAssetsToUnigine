
import os

from def_globals import *

from wand.image import Image
from wand.color import Color


def ImageConvert(img, dest_path):
	'''

	CorruptImageError
	'''

	if (DEBUG_DISABLE_IMAGE_CONV): return	# Debug disable.

	from wand.image import Image
	from wand.color import Color

	filename, file_extension = os.path.splitext(os.path.basename(img))
	new_filename = convert_suffixes_to_unigine(filename)
	
	try:
		original = Image(filename = img)
		converted = original.convert('tga')

		if (filename.endswith("_diff")):
			# albedo (RGB, RGB+A)
			pass

		if (filename.endswith("_ddna")):
			# normalmap (RG)
			converted.alpha_channel = 'off'

			# shading (R-metalness, G-roughness, B-specular)
			alpha_image = original.clone()
			alpha_image.alpha_channel = 'extract'
			alpha_image.convert('RGB')
			
			gloss_img = original.clone()
			gloss_img.alpha_channel = 'off'
			gloss_img.composite_channel("green", alpha_image, 'copy')
			gloss_img.level(1, 0, 0.0, 'red') #fill red channel black
			gloss_img.level(1, 0, 0.0, 'blue')

			sh_filename = new_filename[:-5] + "_sh" + ".tga"
			exported_file = os.path.join(dest_path, sh_filename)
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

		converted.save(filename = exported_file)

	except Exception:
		logging.error("\nWand exception on texture: " + img + "\n")
	
	pass


def ImageMagicConvertBySet(imgs, dest_path):
	'''

	'''
	converted_images = []
	

	return converted_images

