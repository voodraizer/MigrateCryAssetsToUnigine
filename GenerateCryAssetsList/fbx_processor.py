import sys
import os
# sys.path.append("c:/Python/Python37/Lib/site-packages/fbxdk")


try:
	from FbxCommon import *
except ImportError:
	print("Error: module FbxCommon module failed to import.\n")
	print("Copy the files located in the compatible sub-folder lib/python<version> into your python interpreter site-packages folder.")
	import platform
	if platform.system() == 'Windows' or platform.system() == 'Microsoft':
		print('For example: copy ..\\..\\lib\\Python27_x64\\* C:\\Python27\\Lib\\site-packages')

from fbx import *

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


def Remove_fbx_collision(lScene):
	'''
	Find and remove node with collision (mesh or material).

	'''

	lNode = lScene.GetRootNode()
	if (not lNode):
		return

	for i in range(lNode.GetChildCount()):
		lChildNode = lNode.GetChild(i)
		if (not lChildNode):
			continue
		
		mat_count = lChildNode.GetMaterialCount()
		if (mat_count == 1):	# Only one material per mesh support.
			material = lChildNode.GetMaterial(0)
			if (not material):
				continue

			mat_name = material.GetName()
			if (mat_name == "unnamed" or ("collision" in mat_name)):
				print("Node: " + lChildNode.GetName() + " Material: " + mat_name)
				# lMat = material.GetNodeAttribute()
				lChildNode.RemoveMaterial(material)
				pass
		
		node_name = lChildNode.GetName()
		if (node_name.startswith("UCX_") or ("collision" in node_name)):
			print("FOUND COLLISION in " + node_name)
			lMesh = lChildNode.GetNodeAttribute()
			lChildNode.RemoveNodeAttribute(lMesh)
			lNode.RemoveChild(lChildNode)
			pass


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


def Test_fbx_1(path, fbx_file):
	'''
	

	'''

	# Prepare the FBX SDK.
	lSdkManager, lScene = InitializeSdkObjects()
	lResult = LoadScene(lSdkManager, lScene, os.path.join(path, fbx_file))

	if not lResult:
		print("\n\nAn error occurred while loading the scene...")
		return
	
	# Find node with collision (mesh or material).
	Remove_fbx_collision(lScene)

	# Rename materials.
	# Rename_fbx_materials(lScene)

	# Apply scale transform.

	
	# Save fbx.
	# TODO: save as binary
	SaveScene(lSdkManager, lScene, os.path.join(path, "output.fbx"))
		
	# Destroy all objects created by the FBX SDK.
	lSdkManager.Destroy()



#
fbx_path = "c:/GITs/MigrateCryAssetsToUnity/GenerateCryAssetsList/__EXAMPLES"
fbx_file = "Tractor.fbx"
# Split_mesh_by_material(fbx_path, fbx_file)
Test_fbx_1(fbx_path, fbx_file)