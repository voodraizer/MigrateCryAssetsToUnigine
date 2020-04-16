import sys
import os

from def_globals import *


try:
	from FbxCommon import *
except ImportError:
	print("Error: module FbxCommon module failed to import.\n")
	print("Copy the files located in the compatible sub-folder lib/python<version> into your python interpreter site-packages folder.")
	import platform
	if platform.system() == 'Windows' or platform.system() == 'Microsoft':
		print('For example: copy ..\\..\\lib\\Python27_x64\\* C:\\Python27\\Lib\\site-packages')

from fbx import *


# =============================================================================
# 
# =============================================================================
num_tabs = 0


def print_tabs():
	"""
	Print the required number of tabs.
	"""

	global num_tabs

	for i in range(num_tabs):
		sys.stdout.write("  ")

def get_attribute_type_name(type):
	"""
	Return a string-based representation based on the attribute type.
	"""

	if type == FbxNodeAttribute.eUnknown:
		return "unidentified"
	elif type == FbxNodeAttribute.eNull:
		return "null"
	elif type == FbxNodeAttribute.eMarker:
		return "marker"
	elif type == FbxNodeAttribute.eSkeleton:
		return "skeleton"
	elif type == FbxNodeAttribute.eMesh:
		return "mesh"
	elif type == FbxNodeAttribute.eNurbs:
		return "nurbs"
	elif type == FbxNodeAttribute.ePatch:
		return "patch"
	elif type == FbxNodeAttribute.eCamera:
		return "camera"
	elif type == FbxNodeAttribute.eCameraStereo:
		return "stereo"
	elif type == FbxNodeAttribute.eCameraSwitcher:
		return "camera switcher"
	elif type == FbxNodeAttribute.eLight:
		return "light"
	elif type == FbxNodeAttribute.eOpticalReference:
		return "optical reference"
	elif type == FbxNodeAttribute.eOpticalMarker:
		return "marker"
	elif type == FbxNodeAttribute.eNurbsCurve:
		return "nurbs curve"
	elif type == FbxNodeAttribute.eTrimNurbsSurface:
		return "trim nurbs surface"
	elif type == FbxNodeAttribute.eBoundary:
		return "boundary"
	elif type == FbxNodeAttribute.eNurbsSurface:
		return "nurbs surface"
	elif type == FbxNodeAttribute.eShape:
		return "shape"
	elif type == FbxNodeAttribute.eLODGroup:
		return "lodgroup"
	elif type == FbxNodeAttribute.eSubDiv:
		return "subdiv"
	else:
		return "unknown"


def print_attribute(attribute):
	"""
	Print an attribute.
	"""

	if not attribute:
		return

	typeName = get_attribute_type_name(attribute.GetAttributeType())
	attrName = attribute.GetName()
	print_tabs()

	sys.stdout.write(
		"<attribute type='" + typeName +
		"' name='" + attrName + "'/>\n"
	)


def print_node(node):
	"""
	Print a node, its attributes, and all its children recursively.
	"""

	global num_tabs

	print_tabs()
	nodeName = node.GetName()
	translation = node.LclTranslation.Get()
	rotation = node.LclRotation.Get()
	scaling = node.LclScaling.Get()

	# Print the contents of the node.
	sys.stdout.write(
		"<node name='" + nodeName + "' "
		+ "translation='("
		+ str(translation[0]) + ", "
		+ str(translation[1]) + ", "
		+ str(translation[2]) + ")' "
		+ "rotation='("
		+ str(rotation[0]) + ", "
		+ str(rotation[1]) + ", "
		+ str(rotation[2]) + ")' "
		+ "scaling='("
		+ str(scaling[0]) + ", "
		+ str(scaling[1]) + ", "
		+ str(scaling[2]) + ")'>\n"
	)

	num_tabs += 1

	# Print the node's attributes.
	for i in range(node.GetNodeAttributeCount()):
		print_attribute(node.GetNodeAttributeByIndex(i))

	# Recursively Print the children.
	for j in range(node.GetChildCount()):
		print_node(node.GetChild(j))

	num_tabs -= 1
	print_tabs()
	sys.stdout.write("</node>\n")


# =============================================================================
# 
# =============================================================================
def TriangulateSplitAllMeshes(pScene, pManager):
	lNode = pScene.GetRootNode()
	lConverter = FbxGeometryConverter(pManager)
	
	if lNode:
		for i in range(lNode.GetChildCount()):
			lChildNode = lNode.GetChild(i)
			if lChildNode.GetNodeAttribute() != None:
				lAttributeType = (lChildNode.GetNodeAttribute().GetAttributeType())
			
				if lAttributeType == FbxNodeAttribute.eMesh:
					lMesh = lChildNode.GetNodeAttribute()
				
					print("\nMESH NAME :: %s" % lMesh.GetName())
					print("MESH POLYGONS :: %i" % lMesh.GetPolygonCount())
					print("MESH EDGES :: %i" % lMesh.GetMeshEdgeCount())     
					print("TRIANGULATING MESH")
					lTriangulatedMesh = lConverter.Triangulate(lMesh, False)
					print("\nTRIANGULATING MESH COMPLETED")
					print("TRIANGULATED MESH POLYGONS :: %i" % lTriangulatedMesh.GetPolygonCount())
					print("TRIANGULATED MESH EDGES :: %i" % lTriangulatedMesh.GetMeshEdgeCount())                
				
					lChildNode.RemoveNodeAttribute(lMesh)
					lChildNode.AddNodeAttribute(lTriangulatedMesh)
				
					# Mesh is triangulated, we can now split it per material
					lResult = lConverter.SplitMeshPerMaterial(lTriangulatedMesh, False) 
					#lChildNode.RemoveNodeAttribute(lTriangulatedMesh)       
	pass


def ListAllMeshesCount(pScene):
	print("NUMBER OF GEOMETRIES :: %i" % pScene.GetGeometryCount())
				

def Split_mesh_by_material(path, fbx_file):
	'''

	'''
	# Prepare the FBX SDK.
	lSdkManager, lScene = InitializeSdkObjects()

	# The example can take a FBX file as an argument.
	lResult = LoadScene(lSdkManager, lScene, os.path.join(path, fbx_file))

	if not lResult:
		print("\n\nAn error occurred while loading the scene...")
	else :
		print("BEFORE SPLITTING MESHES")
		ListAllMeshesCount(lScene)
		TriangulateSplitAllMeshes(lScene, lSdkManager)
		
		print("\nAFTER SPLITTING MESHES")            
		ListAllMeshesCount(lScene)
		
		SaveScene(lSdkManager, lScene, os.path.join(path, "output.fbx"))
		
	# Destroy all objects created by the FBX SDK.
	lSdkManager.Destroy()


# =============================================================================
# 
# =============================================================================
def Remove_fbx_collision(lScene):
	'''
	Find and remove node with collision (mesh or material).

	'''

	lNode = lScene.GetRootNode()
	if (not lNode):
		return

	# for i in range(lNode.GetChildCount()):
	# 	lChildNode = lNode.GetChild(i)
	# 	if (not lChildNode):
	# 		continue
		
	# 	mat_count = lChildNode.GetMaterialCount()
	# 	if (mat_count == 1):	# Only one material per mesh support.
	# 		material = lChildNode.GetMaterial(0)
	# 		if (material):
	# 			mat_name = material.GetName()
	# 			if (mat_name == "unnamed" or ("collision" in mat_name)):
	# 				# print("Node: " + lChildNode.GetName() + " Material: " + mat_name)
	# 				# lMat = material.GetNodeAttribute()
	# 				lChildNode.RemoveMaterial(material)
	# 				pass
		
	# 	# attr_type = child.GetNodeAttribute().GetAttributeType()
	# 	# if attr_type == FbxCommon.FbxNodeAttribute.eMesh:
	# 	node_name = lChildNode.GetName()
	# 	print("Node: " + node_name)
	# 	if (node_name.startswith("UCX_") or ("collision" in node_name) or ("proxy" in node_name)):
	# 		print("\t\tFOUND COLLISION in " + node_name)
	# 		lMesh = lChildNode.GetNodeAttribute()
	# 		lChildNode.RemoveNodeAttribute(lMesh)
	# 		lNode.RemoveChild(lChildNode)
	# 		pass

	# for i in range(lNode.GetChildCount()):
	# 	lChildNode = lNode.GetChild(i)
	# 	print_node(lChildNode)

	node_for_delete = []
	for i in range(lNode.GetChildCount()):
		lChildNode = lNode.GetChild(i)
		node_name = lChildNode.GetName()
		if (node_name.startswith("UCX_") or ("collision" in node_name) or ("proxy" in node_name)):
			node_for_delete.append(node_name)

	for node_name in node_for_delete:
		node = lNode.FindChild (node_name, True)
		if (node):
			lNode.RemoveChild(node)


def Rename_fbx_materials(lScene):
	'''
	Rename materials.

	'''

	lNode = lScene.GetRootNode()
	if (not lNode):
		return

	for i in range(lNode.GetChildCount()):
		lChildNode = lNode.GetChild(i)
		node_name = lChildNode.GetName()
		if (node_name.startswith("UCX_")):# or node_name.find("collision") == -1):
			print("FOUND COLLISION in " + node_name)

		if lChildNode.GetNodeAttribute() != None:
			lAttributeType = (lChildNode.GetNodeAttribute().GetAttributeType())
			
			if lAttributeType == FbxNodeAttribute.eMesh:
				lMesh = lChildNode.GetNodeAttribute()
				# print("\nMESH NAME :: %s" % lMesh.GetName())
				# print("MESH POLYGONS :: %i" % lMesh.GetPolygonCount())


def Convert_fbx_model_to_unigine(fbx_orig_path, fbx_exp_path):
	'''
	

	'''
	
	# Prepare the FBX SDK.
	lSdkManager, lScene = InitializeSdkObjects()
	lResult = LoadScene(lSdkManager, lScene, fbx_orig_path)

	if not lResult:
		logging.error("\n\n\tAn error occurred while loading the scene...\n\t\t" + fbx_orig_path + "\n")
		return
	
	# Find node with collision (mesh or material).
	Remove_fbx_collision(lScene)

	# Rename materials.
	# Rename_fbx_materials(lScene)

	# Apply scale transform.

	
	# Save fbx.
	# TODO: save as binary
	# lSdkManager.GetIOSettings().SetBoolProp(EXP_FBX_MATERIAL, True)
	# lSdkManager.GetIOSettings().SetBoolProp(EXP_FBX_TEXTURE, True)
	# lSdkManager.GetIOSettings().SetBoolProp(EXP_FBX_EMBEDDED, True) # or False if you want ASCII
	# and use pFileFormat in the Exporter.Initialize() call.
	SaveScene(lSdkManager, lScene, fbx_exp_path)
	
	# Destroy all objects created by the FBX SDK.
	lSdkManager.Destroy()



#
fbx_orig_path = "c:/GITs/MigrateCryAssetsToUnity/GenerateCryAssetsList/__EXAMPLES/Tractor_a.fbx"
fbx_exp_path = "c:/GITs/MigrateCryAssetsToUnity/GenerateCryAssetsList/__EXAMPLES/out.fbx"
# Split_mesh_by_material(fbx_path, fbx_file)
Convert_fbx_model_to_unigine(fbx_orig_path, fbx_exp_path)