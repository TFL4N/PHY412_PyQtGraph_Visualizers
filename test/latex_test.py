# local code
import sys
import os
here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, '..'))

from latex2image import *


latex2image(r"$\vec{E}$", 'vec_e.png')
latex2image(r"$\vec{k}$", 'vec_k.png')
latex2image(r"$\vec{E}\left(\vec{r},\right)=E_0 \cos\left(kz-\omega t\right)$", 'linear_polarization_eq.png', align_bottom=False)
latex2image(r"$foo_\phi$", 'foo.png', align_bottom=False)
