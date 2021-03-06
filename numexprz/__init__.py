###################################################################
#  Numexpr - Fast numerical array expression evaluator for NumPy.
#
#      License: MIT
#      Author:  See AUTHORS.txt
#
#  See LICENSE.txt and LICENSES/*.txt for details about copyright and
#  rights to use.
####################################################################

"""
Numexpr is a fast numerical expression evaluator for NumPy.  With it,
expressions that operate on arrays (like "3*a+4*b") are accelerated
and use less memory than doing the same calculation in Python.

See:

https://github.com/pydata/numexpr

for more info about it.

"""

# RAM: numexpr seems to be a little challenging to use absolute_imports with
# I get an error in Python 3.4 saying it can't find PyInit_interpreter ...

#from __future__ import (division, absolute_import, print_function)

#from __config__ import show as show_config
from .__config__ import get_info

if get_info('mkl'):
    print( "Using Intel Vectory Math Library for Numexprz" )
    use_vml = True
else:
    use_vml = False

from .cpuinfo import cpu

if cpu.is_AMD() or cpu.is_Intel():
    is_cpu_amd_intel = True
else:
    is_cpu_amd_intel = False

import os, os.path
import platform

from numexprz.expressions import E
from numexprz.necompiler import NumExpr, disassemble, evaluate
#from numexprz.tests import test, print_versions
from numexprz.utils import (
    get_vml_version, set_vml_accuracy_mode, set_vml_num_threads,
    set_num_threads, detect_number_of_cores, detect_number_of_threads)

# Detect the number of cores
# RAM: the functions in util don't update numexpr.ncores or numexpr.nthreads, 
def countPhysicalProcessors():
    
    cpuInfo = cpu.info
    physicalIDs = []
    for J, cpuDict in enumerate( cpuInfo ):
        if not cpuDict['physical id'] in physicalIDs:
            physicalIDs.append( cpuDict['physical id'] )
    return len( physicalIDs )

try:
    ncores = int(cpu.info[0]['cpu cores'])  * countPhysicalProcessors()
    nthreads = ncores
except:
    ncores = detect_number_of_cores()
    nthreads = detect_number_of_threads()

# Initialize the number of threads to be used
if 'sparc' in platform.machine():
    import warnings

    warnings.warn('The number of threads have been set to 1 because problems related '
                  'to threading have been reported on some sparc machine. '
                  'The number of threads can be changed using the "set_num_threads" '
                  'function.')
    set_num_threads(1)
else:
    set_num_threads(nthreads)

# The default for VML is 1 thread (see #39)
set_vml_num_threads(1)

from . import version

dirname = os.path.dirname(__file__)

__version__ = version.version

