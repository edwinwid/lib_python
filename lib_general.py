# -*- coding: utf-8 -*-
#=========================================================================================
# lib_general.py
# V.1.0.0
# N. Edwin Widjonarko
#
# Python functions that I've found useful
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
import logging


# ---- setup logging ----
logger = logging.getLogger(__name__)



# ---- module / package functions ----

def pip_list_all_packages():
	'''	Returns list of all locally installed packages
		Requires pip
		Source: on http://stackoverflow.com/questions/739993/how-can-i-get-a-list-of-locally-installed-python-modules
		Credits to the SO contributors above.
	'''
	import pip
	installed_packages = pip.get_installed_distributions()
	installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
	     for i in installed_packages])
	return installed_packages_list



# ---- file / dir operations ----

def chk_mkdir(dirpath):
	if not os.path.isdir(dirpath):
		os.mkdir(dirpath)
	return os.path.abspath(dirpath)



# ---- list operations ----

def pop_n(list_in, n, LR):
	'''similar to list.pop(), with the following differences:
		* accepts any kind of python iterables (list, tuple, str)
		* return both the popped element(s) and the modified list 
		* pop n consequtive elements from left or right
			n 		: number of elements popped. non-integer input will be converted to int
			LR='L' 	: pop from left, case insensitive
			LR='R'	: pop from right, case insensitive
		* note: if n < len(list), return the whole list as popped elements.
			No error / warning returned.
		* Invalid inputs --> return None
	'''
	try:
		n = int(n)
	except:
		raise ValueError('n must be a number (will be converted to int) (user input = %s) ' %n)
		return None

	if len(list_in) <= n:
		popped = list_in
		remaining = []
	else:
		if LR.upper()=='L':
			popped = list_in[0:n]
			remaining = list_in[n:]
		elif LR.upper()=='R':
			popped = list_in[(len(list_in)-n):]
			remaining = list_in[0: (len(list_in)-n)]
		else:
			raise ValueError('LR must be either "L" or "R" (user input = %s) ' %LR)
			return None
	
	return popped, remaining



#=========================================================================================
# 									VERSION CHANGE
#=========================================================================================
# 06 Jun 2015	| V 1.0.0	|	First version
#=========================================================================================