"""Simple script to view a HDF5 store.

Usage: python3 view.py file key
"""

import pandas as pd
import sys

f = pd.read_hdf(sys.argv[1], sys.argv[2])
print(f)
