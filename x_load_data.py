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
    
    Most of processing time is for generating the pretty print statement.
    
    TODO:
        1) Figure out a way of parsing the scores here rather than in the individual functions.
    """
    
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

#
#-----------------------------------------------------------------------------------------------



#                                           MAIN
#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    #score_dictionary()
    
    dictionary = unpickle_it(pickle_path=SCORE_DATAPATH, be_verbose=False)
    build_an_entry(dictionary)
    