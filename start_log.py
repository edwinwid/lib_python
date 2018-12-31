# -*- coding: utf-8 -*-
#=========================================================================================
# start_log.py
# V.1.0.0
# N. Edwin Widjonarko
#
# This is a generic way to start logging, my preferred way
#
# GOOD REFERENCES that have influenced this code:
#  * https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
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
logger = logging.getLogger(__name__)  # for compatibility w/ logging tree

# ---- 


#=========================================================================================
# 									VERSION CHANGE
#=========================================================================================
# 31 Jul 2018	| V 1.0.0	|	First version
#=========================================================================================