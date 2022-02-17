#!/usr/bin/env python3
"""
Song Search Load All Data
written by: Anne Hamill
created on: 14 February 2022
clean: 0

Driving code which builds the Score Dictionary, and loads it into the database.
"""
#                                           IMPORTS
#-----------------------------------------------------------------------------------------------
from music21_globals    import *

from rhythm_data        import time_signature
from rhythm_data        import meter
from rhythm_data        import value_list
from rhythm_data        import anacrusis
from rhythm_data        import ties

from pitch_data         import key_signature
from pitch_data         import clef
from pitch_data         import melody_range
from pitch_data         import letter_names
from pitch_data         import solfege_names
from pitch_data         import intervals

from other_data         import number_of_parts
from other_data         import measure_length
from other_data         import repeats
from other_data         import lyrics
from other_data         import chords_symbols
from other_data         import slurs
                                


#                                           VARIABLES
#-----------------------------------------------------------------------------------------------





#                                            METHODS
#-----------------------------------------------------------------------------------------------
def score_dictionary():
    """
    Call the constituent modules to build a complete Score Dictionary
    """
    # First make sure that the corpus and metadata are current
    update_metadata_cache()
    
    # Call each data module starting with the file info
    the_data = score_file_info()
    
    # Get the metadata for each module
    my_metadata = access_metadata()
    
    # Each of the rhythm functions
    time_signature(the_data, my_metadata)
    meter(the_data, my_metadata)
    value_list(the_data, my_metadata)
    anacrusis(the_data, my_metadata)
    ties(the_data, my_metadata)
    
    # Pitch functions
    key_signature(the_data, my_metadata)
    clef(the_data, my_metadata)
    melody_range(the_data, my_metadata)
    letter_names(the_data, my_metadata)
    solfege_names(the_data, my_metadata)
    intervals(the_data, my_metadata)
    
    # Other functions
    number_of_parts(the_data, my_metadata)
    measure_length(the_data, my_metadata)
    repeats(the_data, my_metadata)
    lyrics(the_data, my_metadata)
    chords_symbols(the_data, my_metadata)
    slurs(the_data, my_metadata)
    
    pprint(the_data)
    pickle_it(the_data, pickle_path=SCORE_DATAPATH, text_path=SCORE_LOGPATH)

#
#-----------------------------------------------------------------------------------------------




#                                           MAIN
#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    score_dictionary()
    
    