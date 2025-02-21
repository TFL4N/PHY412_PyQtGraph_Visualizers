# local code
import sys
import os
here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, '..'))

from latex2image import *


latex2image(r"$\vec{E}$", 'vec_e.png')
