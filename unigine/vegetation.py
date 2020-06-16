import sys
import os
import logging
import xml.etree.ElementTree as ET

from utils import *

veg_file = r"d:\CRY_MIGRATE\Assets\levels\_samples\sample_woodcut\leveldata\VegetationMap.dat"
# vegbin_file = r"d:\CRY_MIGRATE\Assets\levels\_samples\sample_woodcut\leveldata\VegetationMapBin.dat"
vegbin_file = r"d:\CRY_MIGRATE\Assets\levels\_samples\sample_woodcut\leveldata\VegetationMapBinTest.dat"

# struct SVegInst
# {
# 	Vec3  pos;                  4*3
# 	float scale;                4
# 	int   objectIndex;          4
# 	uint8 brightness;           1
# 	float angle;                4
# 	float angleX;               4
# 	float angleY;               4
# };                            33

def Convert_vegetation():
	# f = open(veg_file, 'r')
	# # l = [line.strip() for line in f]
	# for line in f:
	# 	print(str(line))

	# with open(veg_file, "rb") as f:
	# 	byte = f.read(16)
	# 	while byte:
	# 		# Do stuff with byte.
	# 		byte = f.read(16)
	# 		print(str(byte))


	tree = ET.parse(veg_file)
	root = tree.getroot()

	objects = root.find("Objects")
	for veg_obj in objects.iter("Object"):
		name = xml_get(veg_obj, "FileName")
		# print(name)
		pass

	import struct

	with open(vegbin_file, "rb") as f:
		# byte = f.read(16)
		# while byte:
		# 	# Do stuff with byte.
		# 	byte = f.read(16)
		# 	print(str(byte))
		veg_inst_data = f.read(29)  # skip header

		# while veg_inst_data:
		# 	veg_inst_data = f.read(18) #33
		# 	veg_inst_data = struct.unpack('eeeeeBeee', veg_inst_data)
		# 	# veg_inst_data = f.read(36)
		# 	# veg_inst_data = struct.unpack('fffffBfff', veg_inst_data)
		#
		# 	pos = (veg_inst_data[0], veg_inst_data[1], veg_inst_data[2])
		# 	scale = veg_inst_data[3]
		# 	object_index = veg_inst_data[4]
		# 	brightness = veg_inst_data[5]
		# 	angle = veg_inst_data[6]
		# 	angle_roll = (veg_inst_data[7], veg_inst_data[8])
		# 	print("Pos: " + str(pos) +
		# 	      "\nScale: " + str(scale) +
		# 	      "\nObj indx: " + str(object_index) +
		# 	      "\nBrightness: " + str(brightness) +
		# 	      "\nAngle: " + str(angle) +
		# 	      "\nRoll: " + str(angle_roll) +
		# 	      "\n-----------------------------------")
		pass

		header = f.read(28)
		veg_inst_data = f.read()
		print(veg_inst_data)
		arraySize = len(veg_inst_data)
		print("Size: " + str(arraySize))
		numInst = arraySize / 33
		print("Num inst: " + str(numInst))

		data_struct = 'fffffBfff'
		print("Data size: " + str(struct.calcsize(data_struct)))

		# veg_inst_data = struct.unpack(data_struct, veg_inst_data)
		# pos = (veg_inst_data[0], veg_inst_data[1], veg_inst_data[2])
		# scale = veg_inst_data[3]
		# object_index = veg_inst_data[4]
		# brightness = veg_inst_data[5]
		# angle = veg_inst_data[6]
		# angle_roll = (veg_inst_data[7], veg_inst_data[8])
		# print("Pos: " + str(pos) +
		#       "\nScale: " + str(scale) +
		#       "\nObj indx: " + str(object_index) +
		#       "\nBrightness: " + str(brightness) +
		#       "\nAngle: " + str(angle) +
		#       "\nRoll: " + str(angle_roll) +
		#       "\n-----------------------------------")


	pass

# =============================================================================
#
# =============================================================================
if __name__ == "__main__":
	Convert_vegetation()

	pass