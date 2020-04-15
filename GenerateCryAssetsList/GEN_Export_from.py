import os

from def_globals import *
from CryEngineAssets import *


if (not os.path.exists(os.path.dirname(TMP_EXPORT_ASSETS_PATH))):
		os.makedirs(os.path.dirname(TMP_EXPORT_ASSETS_PATH))


# ParseModels(MODELS_XML)

Create_textures_xml_list(CRYENGINE_ASSETS_PATH)
Create_materials_xml_list(CRYENGINE_ASSETS_PATH)
Create_models_xml_list(CRYENGINE_ASSETS_PATH)
# Create_prefabs_xml_list(CRYENGINE_ASSETS_PATH)
# Create_levels_xml_list(CRYENGINE_ASSETS_PATH)