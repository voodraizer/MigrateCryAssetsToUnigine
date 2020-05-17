import sys
import os

import bpy


path = os.path.dirname(os.path.abspath(__file__))[:-7]
sys.path.append(path)
import def_globals

print(def_globals.DESTINATION_ASSETS_PATH)


def CreateMaterialGeneric(mat_name):
	'''
	Find material by name or create.
	Create material node tree.
	'''
	mat = bpy.data.materials.get(mat_name)
	if (mat is None):
		# create new material
		mat = bpy.data.materials.new(name = mat_name)
		mat.use_nodes = True
		mat.use_fake_user = True

	# delete all nodes
	for m in mat.node_tree.nodes:
		mat.node_tree.nodes.remove(m)
		

	mat_nodes = mat.node_tree.nodes
	mat_links = mat.node_tree.links

	# generate new node tree
	output = mat_nodes.new('ShaderNodeOutputMaterial')
	output.name = "Output"
	output.location = (0, 0)

	bsdf = mat_nodes.new('ShaderNodeBsdfPrincipled')
	bsdf.name = "Bsdf"
	bsdf.location = (-400, 0)
	mat_links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
	

	# albedo
	texture = mat_nodes.new('ShaderNodeTexImage')
	texture.name = "Albedo"
	texture.location = (-800, 50)
	texture.use_custom_color = True
	texture.color = (0.272209, 0.608, 0.378043)

	mat_links.new(texture.outputs['Color'], bsdf.inputs['Base Color'])

	if (bpy.data.images.get('wood_10_alb.tga') == None):
		# bpy.ops.image.open(filepath='D:/wood_10_alb.tga')
		bpy.data.images.load(filepath='D:/wood_10_alb.tga')
	texture.image = bpy.data.images.get('wood_10_alb.tga')


	# normals
	texture = mat_nodes.new('ShaderNodeTexImage')
	texture.name = "Normals"
	texture.location = (-1000, -600)
	texture.use_custom_color = True
	texture.color = (0.272209, 0.608, 0.378043)

	if (bpy.data.images.get('wood_10_n.tga') == None):
		bpy.data.images.load(filepath='D:/wood_10_n.tga')
	texture.image = bpy.data.images.get('wood_10_n.tga')
	texture.image.colorspace_settings.name = 'Non-Color'

	normalmap = mat_nodes.new("ShaderNodeNormalMap")
	normalmap.location = (-700, -600)
	normalmap.uv_map = "UVMap"
	mat_links.new(texture.outputs['Color'], normalmap.inputs['Color'])
	mat_links.new(normalmap.outputs['Normal'], bsdf.inputs['Normal'])


	# shading
	texture = mat_nodes.new('ShaderNodeTexImage')
	texture.name = "Shading"
	texture.location = (-1200, -250)
	texture.use_custom_color = True
	texture.color = (0.272209, 0.608, 0.378043)

	if (bpy.data.images.get('wood_10_sh.tga') == None):
		bpy.data.images.load(filepath='D:/wood_10_sh.tga')
	texture.image = bpy.data.images.get('wood_10_sh.tga')
	texture.image.colorspace_settings.name = 'Linear'

	sep_rgb = mat_nodes.new(type="ShaderNodeSeparateRGB")
	sep_rgb.location = (-900, -300)
	sep_rgb.hide = True
	mat_links.new(texture.outputs['Color'], sep_rgb.inputs['Image'])

	mat_links.new(sep_rgb.outputs['R'], bsdf.inputs['Metallic'])

	maths = mat_nodes.new("ShaderNodeMath")
	maths.location = (-650, -350)
	maths.hide = True
	maths.operation = 'SUBTRACT'
	maths.inputs[0].default_value = 1
	mat_links.new(sep_rgb.outputs['G'], maths.inputs[1])
	mat_links.new(maths.outputs['Value'], bsdf.inputs['Roughness'])

	# texture.colorspace_settings.name = 'Non-Color'

	
	pass


def BlenderDefaultUI():

	# viewport window settings
	bpy.context.space_data.show_gizmo_navigate = False
	bpy.context.space_data.overlay.show_floor = False
	bpy.context.space_data.overlay.show_axis_x = False
	bpy.context.space_data.overlay.show_axis_y = False
	bpy.context.space_data.overlay.show_axis_z = False

	# workspace
	# Window.workspace
	# bpy.ops.object.editmode_toggle()

	# outliner window settings
	bpy.context.space_data.show_restrict_column_viewport = False
	bpy.context.space_data.show_restrict_column_hide = True

	# properties window settings
	bpy.context.space_data.context = 'SCENE'

	# 


	pass


if __name__ == "__main__":
	CreateMaterialGeneric('USDiscoMaterial')

	pass