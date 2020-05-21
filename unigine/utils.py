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


def ListFromString(str, default = [0, 0, 0]):
	list = []

	str = str.split(",")
	if (len(str) < 3): return default

	for s in str:
		list.append(float(s))

	return list


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
	# m = pyrr.matrix44.multiply(m_s, m_t)

	# m_r = Matrix44(pyrr.matrix44.create_from_eulers([math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2])]))
	m_r = Matrix44(pyrr.matrix44.create_from_eulers([math.radians(-rot[0]), math.radians(-rot[2]), math.radians(-rot[1])]))
	# m = Matrix44(pyrr.matrix44.create_from_x_rotation(math.radians(rot[0])))
	# m = Matrix44(pyrr.matrix44.create_from_z_rotation(math.radians(-rot[2])))
	# m = pyrr.matrix44.multiply(m, m_r)

	m = pyrr.matrix44.multiply(m_s, m_r)
	m = pyrr.matrix44.multiply(m, m_t)

	# transform = ArrayToString([m.c1, m.c2, m.c3, m.c4]) # BAD
	transform = ArrayToString([m.r1, m.r2, m.r3, m.r4])

	return transform


def CreateNodeFromFbx(nodes_root, fbx_path, name, pos, rot, scale):
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
				mesh_data.append((mesh_guid))
			pass

		surface = []
		params = root.find("parameters")
		for param in params.iter('parameter'):
			if (param.get("name") == "material_guids"):
				d = param.text.split(",")
				# print(d)
				for s in range(0, len(d), 2):
					surface.append([d[s], d[s + 1]])
			pass

		return mesh_data, surface

	from random import randint

	id = random_with_N_digits(10)

	mesh_data, surface = GetMeshData(fbx_path)
	# if (len(mesh_data) == 0 or len(surface) == 0): return
	# print(str(len(mesh_data)) + " -- " + str(len(surface)))

	for m in range(len(mesh_data)):
		node = ET.SubElement(nodes_root, 'node')
		node.set("type", "ObjectMeshStatic")
		node.set("name", name)
		node.set("id", str(id))

		mesh = ET.SubElement(node, 'mesh_name')
		mesh.text = "guid://" + mesh_data[m]

		if (m < len(surface)):
			s = surface[m]
			surf = ET.SubElement(node, 'surface')
			surf.set("name", s[0])
			surf.set("material", s[1])

		properties = ET.SubElement(node, 'properties')

		transf = "0.70710665 0.68301272 0.18301271 0.0 -0.70710677 0.68301249 0.18301268 0.0 0 -0.25881907 0.96592581 0.0 0 0 0 1.0"
		# transf = GetTransform([0, 0, 0], [15, 0, 45], [1, 1, 1])
		transf = GetTransform(pos, rot, scale)
		# print("Transf: " + transf)
		transform = ET.SubElement(node, 'transform')
		transform.text = transf

	pass


def CreateNodeFromFbx__OLD(nodes_root, fbx_path, name, pos, rot, scale):
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
				mesh_data.append((mesh_guid))
			pass

		surface = []
		params = root.find("parameters")
		for param in params.iter('parameter'):
			if (param.get("name") == "material_guids"):
				d = param.text.split(",")
				for s in range(0, len(d), 2):
					surface.append([d[s], d[s + 1]])
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

	for m in mesh_data:
		mesh = ET.SubElement(node, 'mesh_name')
		mesh.text = "guid://" + m

	for s in surface:
		surf = ET.SubElement(node, 'surface')
		surf.set("name", s[0])
		surf.set("material", s[1])

	properties = ET.SubElement(node, 'properties')

	transf = "0.70710665 0.68301272 0.18301271 0.0 -0.70710677 0.68301249 0.18301268 0.0 0 -0.25881907 0.96592581 0.0 0 0 0 1.0"
	# transf = GetTransform([0, 0, 0], [15, 0, 45], [1, 1, 1])
	transf = GetTransform(pos, rot, scale)
	# print("Transf: " + transf)
	transform = ET.SubElement(node, 'transform')
	transform.text = transf
	pass


def CreateNodeFromDecal():

	pass
