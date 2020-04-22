import os

from def_globals import *
from UnigineAssets import *


logging.basicConfig(filename = LOG_EXPORTTO_FILE, filemode="w", level = logging.INFO)
logging.info("==================================== START ====================================\n\n")

# =============================================================================
# Export to Unigine.
# =============================================================================
# ParseTexturesXmlList()
# ParseMaterialsXmlList()
# ParseModelsXmlList()
Create_prefabs()



logging.info("\n\n==================================== END ====================================")