import sys
sys.path.insert(0, '/home/vova/tools/gallery')

import logging, sys
logging.basicConfig(stream=sys.stderr)

from gallery import app as application

