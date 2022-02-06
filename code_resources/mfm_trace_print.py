#!/usr/bin/env /usr/local/bin/python3

"""
clean 0
mfm_trace_print.py

Created by Jim Kaubisch on 2018-06_20.
Copyright (c) 2018-20 Music for Minors. All rights reserved.
"""

#--------------------------------------------------------------
# ------ Imports   --------------------------------------------
#--------------------------------------------------------------

import traceback
import inspect
from inspect import getframeinfo, stack

from pprint import pprint


#--------------------------------------------------------------
# ------ Variables --------------------------------------------
#--------------------------------------------------------------

# tag for indicating desired placement of the prefix string 
#  e.g. '\n\n{prefsub} The start of processing'
# The prefix string inserted into the printed string is built from 
#       the file name, 
#       line number of the print request,
#       function name,
#       for exception printing, line number where the exception was triggered
#   e.g. mfm_globals.py[202]:abc[200] for an exception 
#           - 'except'ed in globals.com, line 202
#           - caused in function "abc" line 200
#
prefsub = '$prefsub$'


#--------------------------------------------------------------
# ------ Routines  --------------------------------------------
#--------------------------------------------------------------
def debug_print(msg, end='\n', print_it=True):
    """
    stack is a named tuple 
    stack()[0] is current frame (debug_print in this case)
    stack()[0][0]) is the stackframe info, e.g.
        FrameInfo(
        		frame=<frame at 0x7ff001009490, 
        			  file '/Users/jimkaubisch/Dropbox (MFM)/MfMCurrAdmin/Development/_shared_lib/mfm_trace_print.py', 
        			  line 110, 
        			  code <module>
        			 >, 
        		filename='/Users/jimkaubisch/Dropbox (MFM)/MfMCurrAdmin/Development/_shared_lib/mfm_trace_print.py', 
        		lineno=110, 
        		function='<module>', 
        		code_context=[' xyz()\n'], 
        		index=0
        	    )
        
    stack()[1] is our caller 
    """

    debug_stack = False

    if debug_stack:
        print('0\n', stack()[0][0])
        print()
        print('1\n', stack()[1][0])
        print()
        print('-1\n', stack()[-1][0])
        print()

        for index, element in enumerate(stack()):
            print(index)
            pprint(element)
            print()
        
    caller = getframeinfo(stack()[1][0])
    prefix = f'{caller.filename.rsplit("/",1)[-1]}:{caller.function}[{caller.lineno}]: '

    if msg.find(f'{prefsub}') == -1:
        message   = f"{prefix}{msg}"
    else:
        message = msg.replace(prefsub, f"{prefix}")

    if print_it:
        print(message, end=end)

    return message


# -----------------------------------------------------------------
def exception_print(exception_info, print_it=True):
    """
    stack is a named tuple 
    stack()[0] is current frame (debug_print in this case)
    stack()[1] is our caller
    """

    caller = getframeinfo(stack()[1][0])
    err_file = caller.filename.rsplit("/",1)[-1]

    trace = str(traceback.format_exc()).split(",")
    err_lineno = trace[1].rsplit(" ",1)[-1]

    prefix = f'{err_file}[{caller.lineno}]:{caller.function}[{err_lineno}]: '
    prefix_pad = len(prefix)*' '
    template   = "{0}An exception of type {1} occurred. \n{2} - Arguments:{3!r}"
    message = template.format(prefix, type(exception_info).__name__, prefix_pad, exception_info.args)
    
    if print_it:
        print(message)

    return message


#--------------------------------------------------------------
# ------ Test Routines  ---------------------------------------
#--------------------------------------------------------------
def xyz():
    try:
        """
        for index, element in enumerate(stack()):
            print(index)
            pprint(element)
            print()
        """

        debug_print(f'\n...\n,, hello {prefsub} About to do an illegal subscript', True)
        print()
        
        #return
    
        f = 2
        print(f[0])
    except Exception as why:
        exception_print(why)
        raise
#--------------------------------------------------------------
# ------ Main      --------------------------------------------
#--------------------------------------------------------------

if __name__ == '__main__':
    pass
    xyz()
    