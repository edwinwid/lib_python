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
import platform
import getpass
import socket
import shutil
import glob
import subprocess
import logging
import logging.config
import yaml


# ---- setup logging ----
logger = logging.getLogger(__name__)


# =============================================================================
# ---- module / package functions ----
# =============================================================================

def pip_list_all_packages():
	'''	Returns list of all locally installed packages.	Requires pip
		Ref: on http://stackoverflow.com/questions/739993/how-can-i-get-a-list-of-locally-installed-python-modules
		Credits to the SO contributors above.
	--- inputs:
	N/A

	--- return:
	* list of installed package names
	'''
	import pip
	installed_packages = pip.get_installed_distributions()
	installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
		 for i in installed_packages])
	return installed_packages_list

# =============================================================================
# ---- computer info ----
# =============================================================================

def get_os():
	''' Return basic information about the workstation's OS

	--- inputs:
	N/A

	--- return:
	* OS (e.g. Windows)
	* OS release (e.g. XP)
	* OS version (e.g. 5.1)
	'''
	return (platform.system(), platform.release(), platform.version())


def get_username():
	''' Return the current username

	--- inputs:
	N/A

	--- return:
	* username
	'''
	return getpass.getuser()


def get_host():
	''' Return the current host computer ID

	--- inputs:
	N/A

	--- return:
	* hostname
	'''
	return socket.gethostname()


# =============================================================================
# ---- file / dir operations ----
# =============================================================================

def upath(posixpath, host=''):
	''' "universal path". Properly format the input posix path for the current system.

	--- inputs:
	* posixpath 	: file or dir path, posix-style (forward slash)
	* OPT: host 	: mounted file server, to prepend before the path. 
					  e.g. '//HOSTNAME'. Note the double forward slash

	--- return:
	* input path formatted to conform to current OS's style
	'''
	if not os.path.isdir(dirpath):
		os.mkdir(dirpath)
	return os.path.abspath(dirpath)


def chk_mkdir(dirpath):
	''' make a directory if the directory path does not exist 

	--- inputs:
	* directory path

	--- return:
	* directory path
	'''
	if not os.path.isdir(dirpath):
		os.mkdir(dirpath)
	return os.path.abspath(dirpath)


def enumfn(filepath, startinc=0):
	''' enumerate file name with "_n" and auto-increment as necessary
		Note that this function only works on the file name string and does not actually 
		change the file name on disk.

	--- inputs:
	* filepath 		: String representation of the file path. Will be parsed to get base file name, 
						extension, and directory name
	* OPT: startinc : starting enumeration

	--- return:
	* new file name with "_n" suffix
	'''
	basedir = os.path.dirname(filepath)
	basename = os.path.basename(filepath)
	ext = os.path.splitext(basename)[1]
	basename = os.path.splitext(basename)[0]

	auto_inc = startinc
	filename = os.path.join(basedir, (basename + '_' + str(auto_inc) + ext))
	while(os.path.exists(filename)):
		auto_inc += 1
		filename = os.path.join(basedir, (basename + '_' + str(auto_inc) + ext))

	return filename


def copytree(src, dst, symlink=False, ignore=None):
	''' a wrapper for shutil copytree and copy2 to mimic bash copy, i.e. this
		will take both file and directory as src

	--- inputs:
	* src 		: source directory or file
	* dst 		: destination path
	* OPT: synmlink : If True, symbolic links in the source tree are represented as symbolic links 
						in the new tree, but the metadata of the original links is NOT copied; if 
						False or omitted, the contents and metadata of the linked files are copied 
						to the new tree
	* OPT: ignore 	: is a callable defining items to ignore. See shutil documentation for more info

	--- return:
	* NONE
	'''
	for item in os.listdir(src):
		s = os.path.listdir(src, item)
		d = os.path.listdir(dst, item)
		if os.path.isdir(s):
			shutil.copytree(s, d, symlink, ignore)
		else:
			shutil.copy2(s, d)


def searchpath(indir, incRegex, excRegex='', fileOrDir='df'):
	''' Search for file or directory names satisfying incRegex, and excluding those that satisfy
		excRegex.

	--- inputs:
	* indir			: parent directory under which to do the search
	* incRegex		: regex string pattern for the matching path name. Empty string = include all
	* OPT: excRegex : regex string pattern to exclude. Empty string = no exclusion
	* OPT: fileOrDir: 'f'  = only return files
					  'd'  = only return directories
					  'fd' or 'df' = return file and directory names

	--- return:
	* list of path names
	'''
	if not fileOrDir in ['f', 'd', 'fd', 'df']:
		raise ValueError('Valid choice for fileOrDir are: "f", "d", "fd", or "df"')

	all_paths = os.listdir(indir)
	list_path = []

	for path in all_paths:
		pass_fileDir = True
		pass_regex = False

		# file or dir or both
		if fileOrDir=='f':
			pass_fileDir = os.path.isfile( os.path.join(indir, path) )
		elif fileOrDir=='d':
			pass_fileDir = os.path.isdir( os.path.join(indir, path) )

		# evaluate regex
		if incRegex is not '':
			if re.search(incRegex, path):
				if excRegex is not '':
					if not re.search(excRegex, path):
						pass_regex = True
				else:
					pass_regex = True
		else:
			pass_regex = True

		if pass_fileDir and pass_regex:
			list_path.append( os.path.join(indir, path) )


def filelen(filepath):
	''' Get the number of lines in a text file

	--- inputs:
	* filepath		: input file path

	--- return:
	* number of lines
	'''
	f = open(str(fpath), 'r')
	for i, l in enumerate(f):
		pass
	f.close()
	return i + 1


def splitfile(filepath, maxlines=1000, outdir='', header=True):
	''' Split a text file (e.g. csv) into multiple, smaller files. The new file names are
		enumerated from 0.

	--- inputs:
	* filepath		: input file path
	* OPT: maxlines 	: max num of lines inthe new files (default = 1000)
	* OPT: outdir		: output directory, if not the current dir
	* OPT: header 		: if True, the first line is a header line (useful for csv) 

	--- return:
	* list of (output file, number of lines in the file) tuples
	'''
	list_fnew = []
	list_lenfnew = []
	basefn = os.path.basename(filepath)
	ext = os.path.splitext(basefn)[1]
	if not oudtir=='':
		basefn = os.path.join( outdir, os.path.splitext(basefn)[0])
	else:
		basefn = os.path.splitext(basefn)[0]

	fnum = 0
	newfn = basefn + '_' + str(fnum) + ext
	f_old = open(str(filepath), 'r')
	f_new = open(str(filepath), 'w')
	list_fnew.append(os.path.abspath(newfn))
	for i, l in enumerate(f_old):
		f_new.write(l.strip() + '\n')
		if i==0:
			if header:
				header = l.strip() + '\n'
			else:
				header = ''
		if ( (i+1)%maxlines )==0: 	# open new file
			list_lenfnew.append(maxlines)
			f_new.close()
			fnum += 1
			newfn = basefn + '_' + str(fnum) + ext
			f_new = open(str(newfn), 'w')
			list_fnew.append(os.path.abspath(newfn))
			f_new.write(header)
	list_lenfnew.append((i+1)%maxlines)
	f_old.close()
	f_new.close()

	return zip(list_fnew, list_lenfnew)


# =============================================================================
# ---- operations on list / iterables ----
# =============================================================================

def pop_n(list_in, n, LR):
	'''
	similar to list.pop(), with the following differences:
	* accepts any kind of python iterables (list, tuple, str)
	* return both the popped element(s) and the modified list 
	* pop n consequtive elements from left or right
	* note: if n < len(list), return the whole list as popped elements.
		No error / warning returned.
	* Invalid inputs --> return None

	--- inputs:
		n 		: number of elements popped. non-integer input will be converted to int
		LR='L' 	: pop from left, case insensitive
		LR='R'	: pop from right, case insensitive

	--- return:
		* popped iterable
		* remaining iterable	
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


# =============================================================================
# ---- other operations ----
# =============================================================================

def is_num(s):
	'''
	check if the argument is a number. Using try statement is faster than if/else

	--- inputs:
		anything

	--- return:
		boolean if the input is a number	
	'''
	try:
		float(s)
		return True 
	except ValueError:
		return False


def list_diff(a, b):
	'''
	return elements of list a that is NOT in list b

	--- inputs:
	* a 	: list / tuple
	* b 	: list / tuple

	--- return:
	* difference list
	'''
	return list( set(a) - set(b) )


def source_sh(bash_filepath, sh_cmd='bash', timeout_sec=15):
	'''
	mimic sourcing a bash file and get the environment variables. the env variables
	are only available for this python session only

	REQUIRE: bash or csh

	--- inputs:
	* bash_filepath 	: path to a bash (.sh) file
	* OPT: sh_cmd 		: the command to run the shell (bash or csh, default = "bash")
	* OPT: timeout_sec 	: timeout in second (default = 15)

	--- return:
	* none
	'''
	command = ['bash', '-c', 'source %s && env' %bash_filepath]
	proc = subprocess.Popen(command, stdout = subprocess.PIPE)

	for line in proc.stdout:
		(key, _, value) = line.partition("=")
		os.environ[key] = value.rstrip('\n') 	# remove trailing EOL


def img_pixels(x_aspect, y_aspect, max_px=100):
	'''
	Calculate the number of pixels for an image given the x-y aspect and the
	max number of pixel in one dimension

	--- inputs:
	* x_aspect 		: X aspect value to calculate aspect ratio
	* y_aspect		: Y aspect value to calculate aspect ratio
	* OPT: max_px 	: max number of pixel in either x or y (default = 100)

	--- return:
	* number of pixels in X, number of pixels in Y
	'''
	if x_aspect >= y_aspect:
		px_ratio = math.floor(max_px / x_aspect)
	else:
		px_ratio = math.floor(max_px / y_aspect)
	px_x = px_ratio * x_aspect
	px_y = px_ratio * y_aspect

	return px_x, px_y


def tcllist(raw_tcl_list):
	'''
	parse tcl list into python list

	--- inputs:
	* raw_tcl_list 	: string representation of a tcl list

	--- return:
	* python representation of the input list
	'''
	def add_element(cache, element):
		if element!='':
			cache[-1].append(element)
		return ''
	out = []
	cache = [out]
	element = ''
	escape = False

	for char in raw_tcl_list:
		if escape:
			element += char
			escape = False
		elif char=='\\':
			escape = True
		elif char in ['', '\t', '\r', '\n']:
			element = add_element(cache, element)
		elif char == '{':
			a = []
			cache[-1].append(a)
			cache.append(a)
		elif char == '}':
			element = add_element(cache, element)
			cache.pop()
		else:
			element += char
		return out


def read_in_chunks(file_object, chunk_size=1024):
	'''
	Lazy function (generator) to read a file chunk by chunk. Default chunk size is 1k.
	Use for streaming very large file without line end. If have line end, just open and
	read line by line.

	--- inputs:
	* file_object 		: file object, e.g. output of open()
	* OPT: chunk_size 	: chunk size in byte

	--- return:
	* yield the data chunk by chunk
	'''
	while True:
		data = file_object.read(chunk_size)
		if not data:
			break
		yield data


def list_variables(level='local',types=[]):
	'''
	List all local, global, or scope variables in this python session, apply filter by
	data type, and return in terms of list of tuples for more flexible manipulation
	
	NOTE: local may return only the local variables in this function!!!!!!!


	--- inputs:
	* level 		:	* 'local' = local variables
						* 'global' = global variables
						* 'scope' = scope variables
	* OPT: types 	: list of data type to filter. e.g. [str, pd.DataFrame]. If empty 
						will return list of all variables.

	--- return:
	* list of ( variable name, variable reference ) tuples
	'''
	if level=='local':
		variables = locals()
	elif level=='global':
		variables = globals()
	elif level=='scope':
		variables = dir()
	else:
		raise ValueError('level must equal "local", "global", or "scope"')

	# filter the dictionary and turn it into list of tuples
	list_var = []
	for varname, var in list(variables.iteritems()):
		if len(types)>0:
			list_var.append( (varname, var) )
		else:
			for datatype in types:
				if isinstance(var, datatype):
					list_var.append( (varname, var) )
	return list_var


# =============================================================================
# ---- LOGGING ----
# =============================================================================

def setup_logging(	default_path='log_config.yaml',
					default_level=logging.INFO,
					env_key='LOG_CFG'):
	'''
	Edwin's preferred way to startup logging. Based on:
	https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
	
	This way, there are two ways to setup the logging config. 
	1. setup the default_path in our code --> all production log will be here
	2. set up an environment variable env_key

	Method #2 is useful for e.g. debugging or for forking the log. E.g. during
	production, we'd like to debug using a new config file, then this will allow 
	us to call in console (BASH): 
		export LOG_CFG=debug_config.yaml; python module.py 
	
	Log setting will fallback to basicConfig() if there's something wrong with
	the config file.

	Required packages:
	- yaml
	- logging
	- os

	--- inputs:
	* [OPT] default_path : default path to the logging config file (yaml)
							(DEFAULT = log_config.yaml)
	* [OPT] default_level: default logging level (DEFAULT = INFO)
	* [OPT] env_key: default logging level (DEFAULT = INFO)

	--- return:
	* None
	'''

	path = default_path
	value = os.getenv(env_key, None)
	if value:
		path = value
	if os.path.exists(path):
		print( 'Using python logging config file: %s' %(path) )
		with open(path, 'rt') as f:
			config = yaml.safe_load(f.read())
		logging.config.dictConfig(config)
	else:
		print( 'Using python basic config')
		logging.basicConfig(level=default_level)



#=========================================================================================
# 									VERSION CHANGE
#=========================================================================================
# 06 Jun 2015	| V 1.0.0	|	First version
#=========================================================================================