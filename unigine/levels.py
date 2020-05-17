
import sys
import os
import logging
import xml.etree.ElementTree as ET


path = os.path.dirname(os.path.abspath(__file__))[:-7]
sys.path.append(path)
import def_globals


def get_filepaths(directory, extension):
	"""
	"""
	file_paths = []  # List which will store all of the full filepaths.

	for root, directories, files in os.walk(directory):
		for filename in files:
			if filename.endswith("." + extension):
				filepath = os.path.join(root, filename)
				filepath = filepath[len(directory):]
				file_paths.append(filepath)

	return file_paths


def xml_prettify(elem):
	"""
	Return a pretty-printed XML string for the Element.
	"""

	from xml.etree import ElementTree
	from xml.dom import minidom

	rough_string = ElementTree.tostring(elem, 'utf-8')
	reparsed = minidom.parseString(rough_string)
	return reparsed.toprettyxml(indent="  ")


def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def xml_get(node, attr):
	'''
	Get attribute from xml node.
	Return value or ''.
	'''

	res = node.get(attr)

	if (res == None): return ""
	return res


def ListFromString(str):
	list = []

	str = str.split(",")
	for s in str:
		list.append(float(s))

	return list



def GetMeshGuid(fbx_path):
	guid = None

	return guid


def ParseLayerFile(level_path, nodes_root):
	def random_with_N_digits(n):
		range_start = 10 ** (n - 1)
		range_end = (10 ** n) - 1
		return randint(range_start, range_end)

	print("Parse: " + level_path + "\n")

	tree = ET.parse(level_path)
	root = tree.getroot()

	for layer in root.iter('Layer'):
		# print("Layer: " + xml_get(layer, "Name"))
		for obj in layer.iter('Object'):
			# print("Object Type: " + xml_get(obj, "Type") + " Name: " + xml_get(obj, "Name"))
			if (xml_get(obj, "Type") == "Brush"):
				name = xml_get(obj, "Name")
				pos = xml_get(obj, "Pos")
				rot = xml_get(obj, "Rotate")
				scale = xml_get(obj, "Scale")

				pos = pos.replace("'", "").split(",")
				if (len(pos) < 3):
					pos = [0,0,0]
				else:
					pos = [float(pos[0]), float(pos[1]), float(pos[2])]
				rot = rot.replace("'", "").split(",")
				if (len(rot) < 3):
					rot = [0,0,0]
				else:
					rot = [float(rot[0]), float(rot[1]), float(rot[2])]
				scale = scale.replace("'", "").split(",")
				if (len(scale) < 3):
					scale = [1, 1, 1]
				else:
					scale = [float(scale[0]), float(scale[1]), float(scale[2])]

				CreateTestNodeFromFbx(nodes_root, xml_get(obj, "Prefab"), name, pos, rot, scale)


			if (xml_get(obj, "Type") == "Prefab"):
				guid = xml_get(obj, "PrefabGUID")
				pass
			if (xml_get(obj, "Type") == "Decal"):
				pass


	pass


def GetTransform(pos, rot, scale):

	def ArrayToString(arr):
		res = ""
		for a in arr:
			res = res + " " + str(a[0]) + " " + str(a[1]) + " " + str(a[2]) + " " + str(a[3])

		return res

	import pyrr
	from pyrr import Quaternion, Matrix33, Matrix44, Vector3
	import math

	transform = ""

	m = pyrr.Matrix44.identity()

	m_t = Matrix44(pyrr.matrix44.create_from_translation(pos))
	m_s = Matrix44(pyrr.matrix44.create_from_scale(scale))
	m = pyrr.matrix44.multiply(m_s, m_t)

	# m_r = Matrix44(pyrr.matrix44.create_from_eulers([math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2])]))
	m_r = Matrix44(pyrr.matrix44.create_from_eulers([math.radians(-rot[0]), math.radians(-rot[2]), math.radians(-rot[1])]))
	# m = Matrix44(pyrr.matrix44.create_from_x_rotation(math.radians(rot[0])))
	# m = Matrix44(pyrr.matrix44.create_from_z_rotation(math.radians(-rot[2])))
	m = pyrr.matrix44.multiply(m, m_r)

	# transform = ArrayToString([m.c1, m.c2, m.c3, m.c4]) # BAD
	transform = ArrayToString([m.r1, m.r2, m.r3, m.r4])

	return transform


def CreateTestNode(nodes_root):
	def random_with_N_digits(n):
		range_start = 10 ** (n - 1)
		range_end = (10 ** n) - 1
		return randint(range_start, range_end)

	from random import randint

	id = random_with_N_digits(10)

	node = ET.SubElement(nodes_root, 'node')
	node.set("type", "ObjectMeshStatic")
	node.set("name", "TestNodeName")
	node.set("id", str(id))

	mesh = ET.SubElement(node, 'mesh_name')
	mesh.text = "guid://6a246dfde1d057383b3bb1375571dd2a8a6fea81"

	surf = ET.SubElement(node, 'surface')
	surf.set("name", "barrel_02")
	surf.set("material", "3d2ecf7aa8a840c4733e81ab9df503fd76db3c08")

	properties = ET.SubElement(node, 'properties')

	transf = "0.70710665 0.68301272 0.18301271 0.0 -0.70710677 0.68301249 0.18301268 0.0 0 -0.25881907 0.96592581 0.0 0 0 0 1.0"
	transf = GetTransform([0, 0, 0], [15, 0, 45], [1, 1, 1])
	# print("Transf: " + transf)
	transform = ET.SubElement(node, 'transform')
	transform.text = transf
	pass


def CreateTestNodeFromFbx(nodes_root, fbx_path, name, pos, rot, scale):
	def random_with_N_digits(n):
		range_start = 10 ** (n - 1)
		range_end = (10 ** n) - 1
		return randint(range_start, range_end)

	def GetMeshData(fbx_path):
		fbx_path = fbx_path.replace(".cgf", ".fbx")
		meta = def_globals.DESTINATION_ASSETS_PATH + fbx_path + ".meta"
		if (not os.path.exists(meta)): return [], []

		tree = ET.parse(meta)
		root = tree.getroot()

		mesh_data = []
		runtimes = root.find("runtimes")
		for rt in runtimes.iter('runtime'):
			if (rt.get("type") == "1"):
				mesh_guid = rt.get("id")
				print(mesh_guid)
				mesh_data.append((mesh_guid))
			pass

		surface = []
		params = root.find("parameters")
		for param in params.iter('parameter'):
			if (param.get("name") == "material_guids"):
				print(param.text)
				d = param.text.split(",")
				surface.append([d[0], d[1]])
			pass

		return mesh_data, surface

	from random import randint

	id = random_with_N_digits(10)

	mesh_data, surface = GetMeshData(fbx_path)
	if (len(mesh_data) == 0 or len(surface) == 0): return

	node = ET.SubElement(nodes_root, 'node')
	node.set("type", "ObjectMeshStatic")
	node.set("name", name)
	node.set("id", str(id))

	mesh = ET.SubElement(node, 'mesh_name')
	mesh.text = "guid://" + mesh_data[0]

	surf = ET.SubElement(node, 'surface')
	surf.set("name", surface[0][0])
	surf.set("material", surface[0][1])

	properties = ET.SubElement(node, 'properties')

	transf = "0.70710665 0.68301272 0.18301271 0.0 -0.70710677 0.68301249 0.18301268 0.0 0 -0.25881907 0.96592581 0.0 0 0 0 1.0"
	# transf = GetTransform([0, 0, 0], [15, 0, 45], [1, 1, 1])
	transf = GetTransform(pos, rot, scale)
	# print("Transf: " + transf)
	transform = ET.SubElement(node, 'transform')
	transform.text = transf
	pass

def ConvertLevel(level_path, level_name):
	lyr_files = get_filepaths(level_path + level_name, "lyr")

	nodes_root = ET.Element('nodes')
	nodes_root.set("version", "2.11.0.0")

	# CreateTestNode(nodes_root)
	# CreateTestNodeFromFbx(nodes_root, "models/Props/Barrels/Barrel_02a.fbx")

	for layer in lyr_files:
		path = level_path + level_name + layer
		path = path.replace("/", "\\").replace("\\\\", "\\")
		ParseLayerFile(path, nodes_root)
		pass

	node_path = def_globals.DESTINATION_ASSETS_PATH + "level_nodes/" + level_name + ".node"
	if (not os.path.exists(os.path.dirname(node_path))): os.makedirs(os.path.dirname(node_path))

	indent(nodes_root)
	tree = ET.ElementTree(nodes_root)
	tree.write(node_path)

	print("==================================================")
	# print(xml_prettify(tree))
	# print(indent(nodes_root))
	# indent(nodes_root)
	# ET.dump(nodes_root)
	print("==============node====================================")


	pass


def Convert():
	levels_path = def_globals.CRYENGINE_ASSETS_PATH + "levels/_samples/"

	ConvertLevel(levels_path, "sample_woodcut")

	pass


if __name__ == "__main__":
	Convert()

	pass