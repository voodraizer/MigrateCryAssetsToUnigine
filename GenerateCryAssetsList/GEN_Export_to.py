import os

from def_globals import *
from UnigineAssets import *


logging.basicConfig(filename = LOG_EXPORTTO_FILE, filemode="w", level = logging.INFO)
logging.info("==================================== START ==================================== ")

# =============================================================================
# Export to Unigine.
# =============================================================================
# ParseTexturesXmlList(TEXTURES_XML)
ParseMaterialsXmlList(MATERIALS_XML)
ParseModelsXmlList(MODELS_XML)



logging.info("==================================== END ==================================== ")