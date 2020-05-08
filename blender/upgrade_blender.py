import bpy

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
		mat.use_fake_use = True
	else:
		# delete all nodes
		for m in mat.node_tree.nodes:
			mat.node_tree.nodes.remove(m)
		

	mat_nodes = mat.node_tree.nodes
	mat_links = mat.node_tree.links

	# generate new node tree
	output = mat_nodes.new('ShaderNodeOutputMaterial')
	output.location = (0, 0)
	bsdf = mat_nodes.new('ShaderNodeBsdfPrincipled')
	bsdf.location = (-400, 0)
	mat_links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
	
	texture = mat_nodes.new('ShaderNodeTexImage')
	texture.location = (-800, 0)
	mat_links.new(texture.outputs['Color'], bsdf.inputs['Base Color'])


	pass


def UpgradeUI():

	# viewport settings
	bpy.context.space_data.show_gizmo_navigate = False
	bpy.context.space_data.overlay.show_floor = False
	bpy.context.space_data.overlay.show_axis_x = False
	bpy.context.space_data.overlay.show_axis_y = False
	bpy.context.space_data.overlay.show_axis_z = False

	# workspace
	# bpy.ops.object.editmode_toggle()


	pass


if __name__ == "__main__":
	CreateMaterialGeneric('USDiscoMaterial')
	pass