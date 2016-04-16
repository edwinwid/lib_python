#=========================================================================================
# lib_general_pandas.py
# V.1.0.0
# N. Edwin Widjonarko
#
# Generic functions for pandas data frame manipulations
#
#
# ------------------------------------------------------------------------------------
# 									BSD License
# ------------------------------------------------------------------------------------
# Copyright © belongs to N. Edwin Widjonarko
# All rights reserved.
# Redistribution and use in source and binary forms, with or without modification, 
# are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice, this list of 
# 		conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this list 
# 		of conditions and the following disclaimer in the documentation and/or other 
# 		materials provided with the distribution.
# 3. Neither the name of the owner nor the names of its contributors may be used to endorse
# 		or promote products derived from this software without specific prior written 
# 		permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY 
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
# COPYRIGHT HOLDER BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#=========================================================================================

import os, sys
import pandas as pd
import logging


# ---- setup logging ----
logger = logging.getLogger(__name__)



# ---- functions not to be used with df.apply ----



# ---- aux functions for functions to be used with df.apply (main functions below) ----




# ---- df apply functions (to be used with df.apply) ----

def lookup_valrange(df, col_value, df_lookup, col_min, col_max, col_out, ge=True, le=True, firstentry='first'):
	''' For each value in df[col_value], lookup for the range bracket in df_lookup, 
	and return the df[col_out] corresponding to that value range.
	* Outputs string (for consistency). If multiple match, return string representation
		of python list
	* ge = greater than and equal to the value in col_min, otherwise strictly greater than
	* le = less than and equal to the value in col_max, otherwise strictly less than
	* firstentry = behavior when there're duplicate matches:
			* 'first' : get the first match
			* 'last : get the last match
			* 'none' : return string 'DUPLICATE <N duplicates>' when there's duplicate
	EXAMPLE: lookup tax rate.
		* df = dataframe with column 'INCOME'
		* col_value = 'INCOME'
		* df_lookup = tax rate lookup dataframe, with columns 'MIN_INCOME_BRACKET', 'MAX_INCOME_BRACKET',
				'TAX_RATE'. 
				Assume tax bracket info as follows: 'MIN_INCOME_BRACKET' <= INCOME < 'MAX_INCOME_BRACKET'
		* col_min = 'MIN_INCOME_BRACKET'
		* col_max = 'MAX_INCOME_BRACKET'
		* col_out = 'TAX_RATE'
		* ge = False (see assumption on tax bracket above)
		* le = True (see assumption on tax bracket above)
		* firstentry = 'none' (this way we know if there's something wrong with the df_lookup)
	'''
	value = df[col_value]
	try:
		float(value)
	except ValueError:  # if not numeric, return empty string
		return ''

	if firstentry.lower!='first' and firstentry.lower!='last' and firstentry.lower!='none':
		logger.error('Invalid input: firstentry = "%s". Accepted values = "first", "last", or "none"' %firstentry)

	if ge and le:
		query_statement = str(col_min) + ' <= ' + str(value) + ' <= ' + str(col_max)
		df_temp = df_lookup.query( query_statement )
	elif (not ge) and le:
		query_statement = str(col_min) + ' < ' + str(value) + ' <= ' + str(col_max)
		df_temp = df_lookup.query( query_statement )
	elif ge and (not le):
		query_statement = str(col_min) + ' <= ' + str(value) + ' < ' + str(col_max)
		df_temp = df_lookup.query( query_statement )
	else:
		query_statement = str(col_min) + ' < ' + str(value) + ' < ' + str(col_max)
		df_temp = df_lookup.query( query_statement )

	if len( list(df_temp.index)) > 1:
		if firstentry.lower()=='first':
			df_temp = df_temp.drop_duplicates(subset=[col_out], keep='first')
			return str(df_temp.iloc[0][col_out]) 
		elif firstentry.lower()=='last':
			df_temp = df_temp.drop_duplicates(subset=[col_out], keep='last')
			return str(df_temp.iloc[0][col_out]) 
		elif firstentry.lower()=='none':
			return ('DUPLICATE ' + str( len(list(df_temp.index))) )
		else:
			return ''
		return str(df_temp.iloc[0][col_out])  
	elif len( list(df_temp.index)) < 1:
		return ''
	else:
		return str(df_temp.iloc[0][col_out]) 


#=========================================================================================
# 									VERSION CHANGE
#=========================================================================================
# 06 Jun 2015	| V 1.0.0	|	First version
#=========================================================================================