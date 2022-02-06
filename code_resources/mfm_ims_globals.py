#!/usr/bin/env python3

"""
MFM Inventory Management System
Created by: Anne Hamill
Created on: 24 December 2021
Version: DEV 0.5
Copyright 2021 Music for Minors

Description:  Store all the variables and methods needed by more than one module.

Clean: 6.51/10

TODO:
    1) Debug and verbose code
    2) Documentation
    3) Logging
    4) Shared method for locating program data?
"""

#------------------------------------------------------------
#--------------------     IMPORTS     --------------------
#------------------------------------------------------------

import  datetime
import  codecs
import  inspect
import  pickle
import  pprint
import  xlsxwriter

from pathlib         import Path

#------------------------------------------------------------
#--------------------     VARIABLES     --------------------
#------------------------------------------------------------
IMS_DATAPATH           = Path.home().joinpath('MFMDropbox', 'MfMCurrAdmin', 'Development', 'inventory_management', '_Data')
IMS_LOGPATH            = Path.home().joinpath('MFMDropbox', 'MfMCurrAdmin', 'Development', 'inventory_management', '_Logs')

ITEMDICTSTORE          = Path.home().joinpath(IMS_DATAPATH, 'program', 'materials_dict.pkl')
TCHDICTSTORE           = Path.home().joinpath(IMS_DATAPATH, 'program', 'tch_assign.pkl')
CHECKOUTDICTSTORE      = Path.home().joinpath(IMS_DATAPATH, 'program', 'checkout_dict.pkl')

#ITEMDICTSTORE          = Path.home().joinpath('Desktop', 'Python', 'inventory_management', '_Data', 'materials_dict.pkl')
#TCHDICTSTORE           = Path.home().joinpath('Desktop', 'Python', 'inventory_management', '_Data', 'tch_assign.pkl')
#CHECKOUTDICTSTORE      = Path.home().joinpath('Desktop', 'Python', 'inventory_management', '_Data', 'checkout_dict.pkl')

CATEGORIES             = ['Drum Kits', 'Containers', 'Instruments', 'Electronics', 'Books', 'Icons', 'Toys & Props', 'Flash Cards', 'Notation Packets', 'Consumables', 'Unused']
GRADES                 = ['T', 'K', '1', '2', '3', '4', '5', '6', 'SDC 1', 'SDC 2', 'SDC 3']



#------------------------------------------------------------
#--------------------     METHODS     --------------------
#------------------------------------------------------------
def pickle_it(a_structure, pickle_path=None, text_path=None):
    """
    Pickle a data structure.
    """
    try:
        # Pickle the materials dictionary
        with open(pickle_path, 'wb') as the_store:
            pickle.dump(a_structure, the_store)

        # Derive a text file from the pickle created in the previous step and do a formatted print
        with codecs.open(text_path, encoding='utf-8', mode='w') as ITPKL:
            report_pp = pprint.PrettyPrinter(indent=2, width=160, stream=ITPKL)
            print('The Pickled Data Structure:\n', file=ITPKL)
            report_pp.pprint(a_structure)

    # Attempt to figure out why pickling failed miserably.
    except IOError as why:
        caller_name = inspect.stack()[1][3]
        print(f'{caller_name}  trying to save "{pickle_path}"')
        print (f'  - saved_structure: Exception: {why}')
        raise
#
#------------------------------------------------------------
#
def determine_academic_year():
    """
    Find the current academic year.  Pre-requisite to determining the Master Inventory workbook file path.
    """

    # Get the current date.
    now = datetime.datetime.now()

    # For Jul-Dec the academic year = current calendar year
    if now.month in [7, 8, 9, 10, 11, 12]:
        current_year = str(now.year)

    # For Jan-Jun the academic year = previous calendar year
    elif now.month in [1, 2, 3, 4, 5, 6]:
        current_year = str(now.year-1)

    return current_year
#
#------------------------------------------------------------
#
def unpickle_it(pickle_path=None, be_verbose=False):
    """
    Unpickle a data structure.
    """
    try:
        # Retreive the materials_dictionary.
        with open(pickle_path, 'rb') as dict_store:
            materials_dict = pickle.load(dict_store)

            assert isinstance(materials_dict, dict)
            return materials_dict

    # If retreiving fails, attempt to let the user know what happened.
    except Exception as why:
        if be_verbose:
            caller_name = inspect.stack()[1][3]
            print(f'{caller_name}  trying to retrieve "{pickle_path}"')
            print (f'  - new_dict: Exception: {why}')
        raise

#------------------------------------------------------------
#--------------------     CLASSES     --------------------
#------------------------------------------------------------
def workbook_formats():
    """
    Gather all the cell formats for writing Excel sheet forms in one place.
    """
    item_category_format = xlsxwriter.Workbook().add_format({'align': 'center',
                                                                      'valign': 'center',
                                                                      'left': 1,
                                                                      'top': 1,
                                                                      'right': 1,
                                                                      'bg_color': '#E2EFDA',
                                                                      'bold': True,
                                                                      'font_size': 16,
                                                                      'border_color': '#BFBFBF',})
    return item_category_format


#------------------------------------------------------------
#--------------------     MAIN     --------------------
#------------------------------------------------------------

if __name__ == '__main__':
    workbook_formats()
