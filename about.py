#!/usr/bin/env python3
"""
Song Search About Data
written by: Anne Hamill
created on: 12 February 2022
clean: 0

Populate the about dictionary for each score in this format.
    { About:     # will need to come from a db/spreadsheet - some fields will not be filled.
        { Composer:        name (if available),
          Country:         self-explanitory,
          Language:        self-explanitory,
          Genre:           self-explanitory,
          Harmony:         kind of harmony - if any,
          Form:            type  - if any,
          Theme:           what the song is about
        }
"""
#                                           IMPORTS
#-----------------------------------------------------------------------------------------------
import pyexcel

from pprint         import pprint

from music21_globals  import SCORE_DATAPATH
from music21_globals  import SCORE_LOGPATH
from music21_globals  import unpickle_it
from music21_globals  import pickle_it
from music21_globals  import access_metadata
from music21_globals  import define_corpus

#                                            METHODS
#-----------------------------------------------------------------------------------------------







#                                           MAIN
#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    pass