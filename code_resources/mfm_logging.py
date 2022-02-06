#!/usr/bin/env /usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
clean 0
globals.py

Created by  Jim Kaubisch on 2018-06_20.
Copyright (c) 2018 Music for Minors. All rights reserved.
"""

#--------------------------------------------------------------
# ------ Imports   --------------------------------------------
#--------------------------------------------------------------

import os
import sys

import logging
from logging.handlers import RotatingFileHandler

#--------------------------------------------------------------
# ------ Routines  --------------------------------------------
#--------------------------------------------------------------

# Assume we have no ini file
config = None
from configparser import ConfigParser

# No ini file? comment out the next few lines
# Have an ini file? Then copy this code to where ever you want to init the config file handling
#   

# What's the path to the ini file, e.g.
#INI_FILE_PATH = '~/MFMDropbox/MfMCurrAdmin/Development/Music21/musicmatch/musicmatch_config.ini'
INI_FILE_PATH = '~/MFMDropbox/MfMCurrAdmin/Development/MusicMatch/musicmatch/musicmatch_config.ini'
#print(f'os.path.abspath({INI_FILE_PATH})')
config = ConfigParser()

if not config.read(os.path.expanduser(INI_FILE_PATH)):
    raise IOError(f'mfm_globals: config file not found: "{INI_FILE_PATH}"')

# end of config init

#
# --------------------------------------------------------------
#
def get_our_logger(my_name=__name__, my_logger_name=None, my_logger_path=None, the_config=None, console_log_level=None, file_log_level="INFO"):
    """
    This routine establishes
    - two loggers for the __main__ module, and
    - subloggers for all other modules

    The two loggers established are
        1: Console logger with default logging level of DEBUG
        2: Rotating file logger with default logging level of INFO

    INPUT:
        my_name          : The name of the module, which determines the logger to be established
                           and, in the case of sub-modules, the name to be give to the logger

        my_logger_name   : default=None, means use the default logger name found in our the_config file
                           if not None, the name to be given to the logger

        my_logger_path   : default=None, means use the default logger path found in our the_config file

        the_config       : The result of reading in the config file.
                            The file is expected to have a subsection as fillows:
                                [logging]
                                log_path = path to directory holding logs, e.g. ~/MFMDropbox/MfMCurrAdmin/Development/Music21/_Logs
                                log_name = name for THIS log file, e.g. m21_history.log
                                max_name_len = the number of characters for the module name field in the log record
                                    effectively, at least the length of the longest module name, e.g. 25

        console_log_level: The logging level desired; None means no logging to the console
                           A good explanation of logging levels is at https://docs.python.org/3/howto/logging.html

        file_log_level   : The logging level desired; None means no logging to the console
                           The file logging handler is of type "RotatingFileHandler"
                           A good explanation of logging levels is at https://docs.python.org/3/howto/logging.html
                           A good explanation of RotatingFileHandler is at 
                                https://docs.python.org/3/library/logging.handlers.html#logging.handlers.RotatingFileHandler
    RETURNS:
        logger: The created logger
    
    Sample Calling code:
    
        logger = get_our_logger(__name__,                       # if we're the __main__ module
                                'MfmMiscMatch test', 
                                console_log_level=None,
                                file_log_level="INFO") \
                                if __name__ == '__main__' \
            else get_our_logger()                               # if this is an imported module
                                                                #  NOTE: this the same as "get_our_logger(__name__)"

        This allows us to "automatically" have different loggers for testing, 
        but all modules imported will have sub-level loggers
    """

    DEBUG_CHOICE = False
    DEBUG = False
    
    LOGPATH = None
    #print(f'get_our_logger: the_config = "{the_config}""')

    # If we're being called as the __main__ module, we need to define our root logger
    if my_name == '__main__':
        #
        # get the actual name of our "__main__" module
        #
        import inspect
        caller_filename = inspect.stack()[1][1].split('/')[-1]
        caller_module_name = caller_filename.rsplit('.',1)[0]

        logger_name = None
        if DEBUG:
            print(f'get_our_logger: creating logger "{caller_module_name}"')

        
        # - Does the_config exist and is is not None?
        if my_logger_path:
            try:
                LOGPATH = my_logger_path
                if DEBUG_CHOICE:
                    print(f'get_our_logger:    makedirs to "{LOGPATH}"')

                # create the LOGPATH if necessary
                #
                os.makedirs(LOGPATH, exist_ok=True)
            except KeyError as why:
                print(f'get_our_logger: Get log path from my_logger_path "{my_logger_path}": - {why} not defined')
                raise KeyError(f'Get log path from my_logger_path "{my_logger_path}": - {why} not defined')
            
        if the_config:
            # Get LOGPATH from the ini file
            #  NOTE: The path in the ini file should be relative to the caller's home directory
            #           i.e. NOT start with "~" or "~user" (path to your home directory)
            #        so the code can be run by another user later
            #
            
            if not LOGPATH:
                try:
                    log_path = the_config["logging"]["log_path"]
                    if not log_path.startswith('~/'):
                        log_path = os.path.join('~', log_path)
                    LOGPATH = os.path.expanduser(log_path)
                    if DEBUG_CHOICE:
                        print(f'get_our_logger:    makedirs to "{LOGPATH}"')

                    # create the LOGPATH if necessary
                    #
                    os.makedirs(LOGPATH, exist_ok=True)
                except KeyError as why:
                    print(f'get_our_logger: Get log path from the_config file: - {why} not defined')
                    raise KeyError(f'Get log path from the_config file: - {why} not defined')

                # Get the LOGFILE from ini file
                # NOTE: By convention, the filename should end with '.log'
                #
                try:
                    logger_name_used = the_config["logging"]["log_name"]
                    LOGFILE = os.path.join(LOGPATH, logger_name_used)
                    if DEBUG_CHOICE:
                        print(f'get_our_logger:    LOGFILE path/name is "{LOGFILE}"')
                except KeyError as why:
                    print(f'get_our_logger: Get logfile name from the_config file: - {why} not defined')
                    raise KeyError(f'Get logfile name from the_config file: - {why} not defined')
            
            # How long does the module name field in a log entry need to be so that the longest name is accomodated?
            #
            try:
                max_name_len = the_config["logging"]["max_name_len"]
                if DEBUG_CHOICE:
                    print(f'get_our_logger:    max_name_len is "{max_name_len}"')
            except KeyError as why:
                raise KeyError(f'get_our_logger: Get max_name_len from the_config file: - {why} not defined')
        else:
            print(f'get_our_logger: logger not defined')
            raise NameError('logger not defined')
        
        # What do we want the log records to look like
        #
        log_entry_format = f'%(asctime)s| %(levelname)-7s | %(module)-{max_name_len}s | %(lineno)4d | %(message)s '
        log_date_format  = '%Y-%m-%d %H:%M:%S'

        if DEBUG:
            print(f'get_our_logger: my_name        : {my_name}')
            #print(f'get_our_logger: logging_path   : {logging_path}')
            #print(f'get_our_logger: default_logfile: {default_logfile}')

        #
        # finally, we're ready to create the logger that will handle all log levels
        #
        if my_logger_name:
            # Our caller wants a non-default logger
            alternate_logger_name = my_logger_name if my_logger_name.endswith('.log') else my_logger_name + '.log'
            if DEBUG_CHOICE:
                print(f'get_our_logger: created alternate root logger as "{alternate_logger_name}"')

            logger_name_used = alternate_logger_name
            LOGFILE = os.path.join(LOGPATH, alternate_logger_name)

            if DEBUG_CHOICE:
                print(f'get_our_logger:    created "{LOGFILE}"')
        
        # What we want our log messages to look like
        #
        mfm_format = logging.Formatter(fmt=log_entry_format, datefmt=log_date_format)

        # create the logger that will handle all log levels
        new_logger = logging.getLogger()
        new_logger.setLevel(logging.DEBUG)

        # create a console handler, set its log level to DEBUG, and add it to the logger
        #
        if console_log_level:
            ch = logging.StreamHandler()
            ch.setFormatter(mfm_format)
            ch.setLevel(eval(f'logging.{console_log_level}'))
            new_logger.addHandler(ch)

        # create a rotating file handler, set its log level to INFO, and add it to the logger
        #   - file to use =  LOGFILE,
        #   - mode='a'       (append mode, i.e. subsequent app executions will add logs to end; also, if doesn't exist, it will be created),
        #   - maxBytes=40000 (max characters before closing this file and opening a new empty one),
        #   - backupCount=2  (max number of log files to keep)
        #   - using formatting string
        #
        if file_log_level:
            rfh = RotatingFileHandler(LOGFILE, mode='a', maxBytes=40000, backupCount=2)
            rfh.setFormatter(mfm_format)
            rfh.setLevel(eval(f'logging.{file_log_level}'))
            new_logger.addHandler(rfh)

        # log a "I've started" message and return the __main__ logger
        #
        #
        new_logger.info(f'Initialized logger {logger_name_used} for module "{caller_module_name}"')
        return new_logger

    # return a sub-level logger for the calling module
    if DEBUG_CHOICE:
        print(f'get_our_logger: returning sub-level logger "{my_name}"')

    return logging.getLogger(my_name)


#--------------------------------------------------------------
# ------ Main      --------------------------------------------
#--------------------------------------------------------------

if __name__ == '__main__':
    logger = get_our_logger(my_name=__name__, my_logger_name='test123', console_log_level="WARNING", file_log_level="INFO")
    
    
    