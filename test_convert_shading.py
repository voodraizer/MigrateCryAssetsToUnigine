
import os

import wand
from wand.image import Image
from wand.color import Color


def ImageMagicConvert():
	'''

	'''
	from wand.image import Image
	from wand.color import Color
	from wand.display import display

	dest_path = "D:/"
	test_file = "d:/___TMP_CRY_ASSETS/Assets/models/Nature/Trees/Big/Textures/Tree10_ddna.tif"
	filename, file_extension = os.path.splitext(os.path.basename(test_file))
	base_filename = filename[0:-5]

	original = Image(filename = test_file)
	gloss_img = original.clone()
	# gloss_img.type = 'grayscale'
    # gloss_img.depth = 8
	gloss_img.alpha_channel = 'off'

	converted = original.convert('tga')
	# converted.format = 'tga'

	
	# gloss_img.composite_channel("green", original, 'copy')
	
	# =================================================================================
	# gloss_img = converted.fx("p.g:0", channel="red") #fill red channel
	# gloss_img = gloss_img.fx("p.g:0", channel="blue")
	# gloss_img.alpha_channel = 'off'

	# gloss_img.level(0, 0, 1.0, 'red') #fill red channel white
	# gloss_img.level(1, 0, 0.0, 'red') #fill red channel black
	# gloss_img.level(1, 0, 1.0, 'red') #invert red channel
	# =================================================================================
	
	
	
	
	alpha_image = original.clone()
	alpha_image.alpha_channel = 'extract'
	alpha_image.convert('RGB')
	gloss_img.composite_channel("green", alpha_image, 'copy')
	gloss_img.level(1, 0, 0.0, 'red') #fill red channel black
	gloss_img.level(1, 0, 0.0, 'blue')
	
	# display(gloss_img)
	# return


	from wand.api import library
	
	# display image
	# from wand.display import display
	# display(gloss_img)

	# alpha_image = converted.channel_images['alpha']
	# with converted.channel_images['red'] as alpha_image:
	# 	alpha_image
	
	# shading (R-metalness, G-roughness, B-specular)
	exported_file = os.path.join(dest_path, base_filename + "_sh" + ".tga")
	
	gloss_img.save(filename = exported_file)
	

	exported_file = os.path.join(dest_path, base_filename + "_n.tga")
	# converted.alpha_channel = False
	# converted.alpha_channel = 'extract'
	# converted.alpha_channel = 'remove'
	converted.alpha_channel = 'off'
	converted.save(filename = exported_file)

	pass

def Test_2():
	from wand.image import Image, COMPOSITE_OPERATORS
	from wand.drawing import Drawing
	from wand.display import display
	from wand.api import library

	wizard = Image(filename='wizard:')
	rose = Image(filename='rose:')
	
	# for o in COMPOSITE_OPERATORS:
	# 	w=wizard.clone()
	# 	r=rose.clone()
	# 	with Drawing() as draw:
	# 		draw.composite(operator=o, left=175, top=250,width=r.width, height=r.height, image=r)
	# 		draw(w)
	# 		display(w)

	w = wizard.clone()
	# with w.channel_images['red'] as red_image:
	# 	display(red_image)

	# print(list(w.channel_images))  ## OK.

#
# Test_2()
ImageMagicConvert()
