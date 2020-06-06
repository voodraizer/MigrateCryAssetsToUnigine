
import sys
import os
import logging
import xml.etree.ElementTree as ET


path = os.path.dirname(os.path.abspath(__file__))[:-7]
sys.path.append(path)
import def_globals

from utils import *


# region Test
# =============================================================================
#
# =============================================================================
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

# endregion

# =============================================================================
#
# =============================================================================

def ParseLayerFile(level_path, nodes_root):
	print("Parse: " + level_path + "\n")

	tree = ET.parse(level_path)
	root = tree.getroot()

	for layer in root.iter('Layer'):
		for obj in layer.iter('Object'):
			if (xml_get(obj, "Type") == "Brush"):
				name = xml_get(obj, "Name")
				pos = xml_get(obj, "Pos")
				rot = xml_get(obj, "Rotate")
				scale = xml_get(obj, "Scale")

				pos = ListFromString(pos)
				rot = ListFromString(rot)
				scale = ListFromString(scale, [1, 1, 1])

				CreateNodeFromFbx(nodes_root, xml_get(obj, "Prefab"), name, pos, rot, scale)
				pass

			if (xml_get(obj, "Type") == "Prefab"):
				name = xml_get(obj, "Name")
				guid = xml_get(obj, "PrefabGUID")
				pos = xml_get(obj, "Pos")
				rot = xml_get(obj, "Rotate")
				scale = xml_get(obj, "Scale")

				pos = ListFromString(pos)
				rot = ListFromString(rot)
				scale = ListFromString(scale, [1, 1, 1])

				AddNodeFromPrefab(nodes_root, guid, pos, rot, scale)
				pass

			if (xml_get(obj, "Type") == "Decal"):
				name = xml_get(obj, "Name")
				guid = xml_get(obj, "PrefabGUID")
				pos = xml_get(obj, "Pos")
				rot = xml_get(obj, "Rotate")
				scale = xml_get(obj, "Scale")

				pos = ListFromString(pos)
				rot = ListFromString(rot)
				scale = ListFromString(scale, [1, 1, 1])

				CreateNodeFromDecal(nodes_root, mat, depth, pos, rot, scale)
				pass

			if (xml_get(obj, "Type") == "Rope"):
				pass


	pass


# =============================================================================
#
# =============================================================================
def ConvertLevel(level_path, level_name):
	lyr_files = get_filepaths(level_path + level_name, "lyr")

	nodes_root = ET.Element('nodes')
	nodes_root.set("version", "2.11.0.0")

	# CreateTestNode(nodes_root)
	# CreateNodeFromFbx(nodes_root, "models/Props/Barrels/Barrel_02a.fbx")

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
	logging.basicConfig(filename="D:/LOG_LEVELS.txt", filemode="w", level=logging.INFO)
	logging.info("==================================== START ====================================\n\n")

	levels_path = def_globals.CRYENGINE_ASSETS_PATH + "levels/_samples/"

	all_levels = ["sample_woodcut", "sample_train_station_01", "sample_storage_area",
	              "sample_rural_farm", "sample_refinery_plant", "sample_plant_07",
	              "sample_plant_06", "sample_plant_05", "sample_plant_04", "sample_plant_03",
	              "sample_plant_02", "sample_plant_01", "sample_gas_station", "sample_forest_01",
	              "sample_construction_site_01", "sample_bridge_02", "sample_bridge_01",
	              "sample_base", "sample_airbase_01"]

	# ConvertLevel(levels_path, "sample_woodcut")

	for level in all_levels:
		ConvertLevel(levels_path, level)

	logging.info("\n\n==================================== END ====================================")
	pass


# =============================================================================
#
# =============================================================================
if __name__ == "__main__":
	Convert()

	pass