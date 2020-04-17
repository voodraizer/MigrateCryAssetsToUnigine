
import os
from PIL import Image, ImageOps

from def_globals import *



def ImageConvert(img, dest_path):
	'''

	CorruptImageError
	'''

	if (DEBUG_DISABLE_WAND): return	# Debug disable.
	

	filename, file_extension = os.path.splitext(os.path.basename(img))
	new_filename = convert_suffixes_to_unigine(filename)
	
	try:
		original = Image.open(img)
		# print("Format: " + original.format + " Mode:" + original.mode)
		
		r, g, b, a = original.split()
		
		exported_file = os.path.join(dest_path, new_filename + ".tga")

		if (filename.endswith("_diff")):
			# albedo (RGB, RGB+A)
			if (original.mode == "RGB"):
				converted = Image.merge('RGB', (r, g, b))
				converted.save(exported_file, compression = 'tga_rle')
			else:
				converted = Image.merge('RGBA', (r, g, b, a))
				converted.save(exported_file, compression = 'tga_rle')
			pass

		if (filename.endswith("_ddna")):
			# normalmap (RG)
			converted = Image.merge('RGB', (r, g, b))
			converted.save(exported_file, compression = 'tga_rle')

			# shading (R-metalness, G-roughness, B-specular)
			spec_img = None
			spec_path = img[:-8] + "spec.tif"
			print(spec_path)
			if (os.path.exists(spec_path)):
				spec_img = Image.open(spec_path).convert('L')

			black = Image.new('RGB', original.size, (0, 0, 0)).convert('L')
			a = ImageOps.invert(a)

			if (spec_img):
				gloss_img = Image.merge('RGB', (black, a, spec_img))
			else:
				gloss_img = Image.merge('RGB', (black, a, black))

			sh_filename = new_filename[:-5] + "_sh" + ".tga"
			exported_file = os.path.join(dest_path, sh_filename)
			gloss_img.save(exported_file, compression = 'tga_rle')
			pass
		
		if (filename.endswith("_spec")):
			pass
		
		if (filename.endswith("_sss")):
			converted = Image.merge('RGB', (r, g, b))
			converted.save(exported_file, compression = 'tga_rle')
			pass

		if (filename.endswith("_mask")):
			converted = Image.merge('RGB', (r, g, b))
			converted.save(exported_file, compression = 'tga_rle')
			pass
		
		if (filename.endswith("_detail")):
			pass

		if (filename.endswith("_displ")):
			if (original.mode == "RGBA"):
				converted = Image.merge('RGB', (a, a, a))
				converted.save(exported_file, compression = 'tga_rle')
			pass

	except Exception as e:
		logging.error("\nWand exception on texture: " + img + "\n" + str(e) + "\n")
		print(str(e))
	
	pass

