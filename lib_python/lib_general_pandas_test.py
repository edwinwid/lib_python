#=========================================================================================
# lib_analyse_hourly.py
# V 0.1.0
# N. Edwin Widjonarko
#=========================================================================================

import os, sys
import numpy as np
import pandas as pd
import logging
import unittest

from lib_general_pandas import *

# ---- setup logging ----
logger = logging.getLogger(__name__)


# ---- test data ----
df_lookup = pd.DataFrame(
	{ 	'income_min' : [100, 200, 300, 400, 500],
		'income_max' : [199, 299, 399, 499, 599],
		'tax_rate'   : [0.01, 0.02, 0.03, 0.04, 0.05]
	}
)
df_data = pd.DataFrame(
	{	'income' : [152, 405, 387, 222, 700, 87],
		'income2' : ['A', 'B', 'D', 'F', 'V', 'X']
	}
)

# --- lookup_valrange ---



df_data['tax'] = df_data.apply(lookup_valrange, axis=1, args=('income2', df_lookup, 'income_min', 'income_max', 'tax_rate'))


print df_data



#=========================================================================================
# 									VERSION CHANGE
#=========================================================================================
# 06 Jun 2015	| V 0.1.0	|	First version, beta
#=========================================================================================