
import os
from PIL import Image, ImageOps

from def_globals import *



def ImageConvert(img, dest_path):
	'''

	CorruptImageError
	'''

	if (DEBUG_DISABLE_IMAGE_CONV): return	# Debug disable.
	

	filename, file_extension = os.path.splitext(os.path.basename(img))
	new_filename = convert_suffixes_to_unigine(filename)
	
	try:
		original = Image.open(img)
		# print("Format: " + original.format + " Mode:" + original.mode)

		black = Image.new('RGB', original.size, (0, 0, 0)).convert('L')		
		
		r, g, b, a = black, black, black, black
		if (original.mode == "RGB"):
			r, g, b = original.split()
		else:
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
			
			if (os.path.exists(spec_path)):
				spec_img = Image.open(spec_path).convert('L')

			a = ImageOps.invert(a)

			if (spec_img):
				gloss_img = Image.merge('RGB', (black, a, spec_img))
			else:
				gloss_img = Image.merge('RGB', (black, a, black))

			# sh_filename = new_filename[:-5] + "_sh" + ".tga"
			# sh_filename = convert_suffixes_to_unigine(new_filename.replace("_n", "_sh"))
			# exported_file = os.path.join(dest_path, sh_filename)
			exported_file = exported_file.replace("_n", "_sh")
			gloss_img.save(exported_file, compression = 'tga_rle')
			pass
		
		if (filename.endswith("_spec")):
			pass
		
		if (filename.endswith("_sss") or filename.endswith("_mask") or filename.endswith("_detail")):
			converted = Image.merge('RGB', (r, g, b))
			converted.save(exported_file, compression = 'tga_rle')
			pass
		
		if (filename.endswith("_blend")):
			if (original.mode == "RGB"):
				converted = Image.merge('RGB', (r, g, b))
				converted.save(exported_file, compression = 'tga_rle')
			pass
		if (filename.endswith("_detail")):
			if (original.mode == "RGB"):
				converted = Image.merge('RGB', (r, g, b))
				converted.save(exported_file, compression = 'tga_rle')
			else:
				converted = Image.merge('RGBA', (r, g, b, a))
				converted.save(exported_file, compression = 'tga_rle')
			pass

		if (filename.endswith("_displ")):
			if (original.mode == "RGBA" or original.mode == "RGBX"):
				converted = Image.merge('RGB', (a, a, a))
				converted.save(exported_file, compression = 'tga_rle')
			pass

	except Exception as e:
		logging.error("\nPillow exception on texture: " + img + "\n" + str(e) + "\nFormat: " + original.format + " Mode:" + original.mode + "\n")
	
	pass

