import sys
import os
import logging
import xml.etree.ElementTree as ET


path = os.path.dirname(os.path.abspath(__file__))[:-7]
sys.path.append(path)
import def_globals

from utils import *


def CreateTestPrefab():
	pref_path = def_globals.CRYENGINE_ASSETS_PATH + "prefabs/buildings.xml"

	tree = ET.parse(pref_path)
	root = tree.getroot()

	for pref in root.iter("Prefab"):
		pref_name = pref.get("Name")
		if (pref_name == "Wood.Wood_03b"):
			nodes_root = ET.Element('nodes')
			nodes_root.set("version", "2.11.0.0")

			dummy = ET.SubElement(nodes_root, 'node')
			dummy.set("type", "NodeDummy")
			dummy.set("id", "622023562")
			dummy.set("name", pref_name.split(".")[-1])

			for obj in pref.iter("Object"):
				pos = xml_get(obj, "Pos")
				rot = xml_get(obj, "Rotate")
				scale = xml_get(obj, "Scale")

				pos = ListFromString(pos)
				rot = ListFromString(rot)
				scale = ListFromString(scale, [1, 1, 1])

				CreateNodeFromFbx(dummy, xml_get(obj, "Prefab"), xml_get(obj, "Name"), pos, rot, scale)

			pref_name = pref_name.split(".")
			pref_path = def_globals.DESTINATION_ASSETS_PATH + "prefabs/" + os.path.basename(pref_path[:-4]) + "/"
			loc_path = pref_name[:-1]
			for p in loc_path:
				pref_path = pref_path + p + "/"
			pref_path = pref_path + pref_name[-1] + ".node"

			print(pref_path)
			indent(nodes_root)
			tree = ET.ElementTree(nodes_root)

			# if (not os.path.exists(os.path.dirname(pref_path))): os.makedirs(os.path.dirname(pref_path))
			# tree.write(pref_path)

			print("==================================================")
			# print(xml_prettify(tree))
			# print(indent(nodes_root))
			# indent(nodes_root)
			# ET.dump(nodes_root)
			print("==============node====================================")

		pass
	pass


def CreateTestPrefab2():
	import xml.etree.ElementTree as ET

	xml_str = '''
<nodes version="2.11.0.0">
	<node type="ObjectMeshStatic" id="1875505392" name="Cuboid">
		<mesh_name>guid://47595c25764c5f40f983499f67f60a729138e729</mesh_name>
		<surface name="box" physics_friction="1" physics_restitution="1" material="cd7481db00c6468ea887becf746f75afc391b964" />
		<transform>1 0 0 0.0 0 1 0 0.0 0 0 1 0.0 0 0 0 1.0</transform>
		<node material="40c5c8b9ddfacc2496922c93e9cb03359ea0c6a8" type="DecalOrtho" id="1726391148" name="DecalOrtho">
			<radius>0.200000003</radius>
			<width>2</width>
			<height>1.5</height>
			<znear>0.00100000005</znear>
			<transform>1 0 0 0.0 0 -1.1920925e-07 0.99999958 0.0 0 -0.99999958 -1.1920925e-07 0.0 0.00010681152 -0.3000412 0.29999977 1.0</transform>
		</node>
	</node>
</nodes>
	'''

	xml_str = '''
	<nodes version="2.11.0.0">
		<node type="ObjectMeshStatic" id="1875505392" name="bricks_house_01a1">
			<mesh_name>guid://35c59a2ac0fe8381495a06ec81cf555bc5db8afe</mesh_name>
			<surface name="Bricks_house_01_bricks" physics_friction="1" physics_restitution="1" material="cd7481db00c6468ea887becf746f75afc391b964" />
			<transform>1 0 0 0.0 0 1 0 0.0 0 0 1 0.0 0 0 0 1.0</transform>
		</node>
	</nodes>
		'''

	tree = ET.ElementTree(ET.fromstring(xml_str))

	root = tree.getroot()
	indent(root)
	tree = ET.ElementTree(root)
	tree.write("d:/UNIGINE Projects/0AZ/data/___TEST/GEN_2.node")

	pass


def CreatePrefabs():
	logging.basicConfig(filename="D:/LOG_PREFABS.txt", filemode="w", level=logging.INFO)
	logging.info("==================================== START ====================================\n\n")

	prefab_all = ["prefabs/bridges.xml", "prefabs/buildings.xml"]

	for path in prefab_all:
		pref_path = def_globals.CRYENGINE_ASSETS_PATH + path

		tree = ET.parse(pref_path)
		root = tree.getroot()

		for pref in root.iter("Prefab"):
			pref_name = pref.get("Name")

			nodes_root = ET.Element('nodes')
			nodes_root.set("version", "2.11.0.0")

			dummy = ET.SubElement(nodes_root, 'node')
			dummy.set("type", "NodeDummy")
			dummy.set("id", "622023562")
			dummy.set("name", pref_name.split(".")[-1])

			for obj in pref.iter("Object"):

				type = xml_get(obj, "Type")

				pos = xml_get(obj, "Pos")
				rot = xml_get(obj, "Rotate")
				scale = xml_get(obj, "Scale")

				pos = ListFromString(pos)
				rot = ListFromString(rot)
				scale = ListFromString(scale, [1, 1, 1])

				if (type == "Brush"):
					CreateNodeFromFbx(dummy, xml_get(obj, "Prefab"), xml_get(obj, "Name"), pos, rot, scale)

				if (type == "Decal"):
					mat = xml_get(obj, "Material")
					s_prior = xml_get(obj, "SortPriority")
					depth = xml_get(obj, "ProjectionDepth")
					CreateNodeFromDecal(dummy, mat, depth, pos, rot, scale)


			indent(nodes_root)
			tree = ET.ElementTree(nodes_root)

			pref_path = GetNodePathFromPrefabName(path, pref_name)

			if (not os.path.exists(os.path.dirname(pref_path))): os.makedirs(os.path.dirname(pref_path))
			tree.write(pref_path)

			print("==================================================")
			# print(pref_path)
			# ET.dump(nodes_root)
			print("==================================================")

		pass

	logging.info("\n\n==================================== END ====================================")
	pass

# =============================================================================
#
# =============================================================================
if __name__ == "__main__":
	# CreateTestPrefab()
	# CreateTestPrefab2()

	# CreatePrefabs()
	pass