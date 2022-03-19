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

from other_data         import *
from pitch_data         import *
from rhythm_data        import *


#                                           VARIABLES
#-----------------------------------------------------------------------------------------------





#                                            METHODS
#-----------------------------------------------------------------------------------------------
def score_dictionary():
    """
    Take the score dictionary with only file information entries, iterate through it to create a full entry.
    
    Most of processing time is for generating the pretty print statement.
    
    TODO:
        1) Figure out a way of parsing the scores here rather than in the individual functions.
    """
    dictionary = score_file_info()
    my_metadata = access_metadata()
    
    for next_entry in dictionary:
        
        # Other musical elements
        dictionary[next_entry]['Other'] = {}
        
        number_of_parts(dictionary, next_entry)
        measure_length(dictionary, next_entry)
        repeats(dictionary, next_entry)
        lyrics(dictionary, next_entry)
        chords_symbols(dictionary, next_entry)
        slurs(dictionary, next_entry)
        
        # Pitch elements
        dictionary[next_entry]['Pitch'] = {}
        
        key_signature(dictionary, my_metadata, next_entry)
        find_clef(dictionary, next_entry)
        melody_range(dictionary, next_entry)
        letter_names(dictionary, next_entry)
        solfege_names(dictionary, next_entry)
        intervals(dictionary, next_entry)
        
        # Rhythm elements
        dictionary[next_entry]['Rhythm'] = {}
        
        time_signature(dictionary, my_metadata, next_entry)
        meter(dictionary, next_entry)
        value_list(dictionary, next_entry)
        anacrusis(dictionary, next_entry)
        ties(dictionary, next_entry)
        
        # About elements
        # will be added at a later time
        
    pickle_it(dictionary, pickle_path=SCORE_DATAPATH, text_path=SCORE_LOGPATH)
    pprint(dictionary)
    return dictionary



#                                           MAIN
#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    score_dictionary()
    

    