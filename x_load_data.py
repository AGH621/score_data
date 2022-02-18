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

"""from rhythm_data        import time_signature
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
from other_data         import slurs"""
                                


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
def xxxbuild_single():
    """
    Build a single entry in the Score Dictionary.
    """
    my_metadata = access_metadata()
    
    score_list = []
    
    for x in range(len(my_metadata)):
        score_path = my_metadata[x].metadata.sourcePath
        file_name = score_path.split('/')[-1].split('.')[0]
        score_list.append(file_name)
        

    # Is there a Score Dictionary already?
    score_dict_path = find_file('score_dictionary.pkl', 'score_data')
    
    # Yes? Unpickle it.
    if score_dict_path:
        pprint(score_dict_path)
        score_dictionary = unpickle_it(pickle_path=SCORE_DATAPATH, be_verbose=False)
    
    # No? Then all the scores need to go into the iteration list.
    else:
        print('not here dave')
        iteration_list = score_list
        pprint(iteration_list)

#
#-----------------------------------------------------------------------------------------------
def build_an_entry(dictionary):
    """
    Take the score dictionary with only file information entries, iterate through it to create a full entry.
    """
    
    for next_entry in dictionary:
        #pprint(dictionary[next_entry])
        
        dictionary[next_entry]['Other'] = {}
        number_of_parts(dictionary, next_entry)
        measure_length(dictionary, next_entry)
    
    pprint(dictionary)

#
#-----------------------------------------------------------------------------------------------



#                                           MAIN
#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    #score_dictionary()
    
    dictionary = unpickle_it(pickle_path=SCORE_DATAPATH, be_verbose=False)
    build_an_entry(dictionary)
    