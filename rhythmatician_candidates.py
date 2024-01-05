#!/usr/bin/env python3

"""
Simple Data Request

Query the Type dictionary
    how many types of:
        regular notes
        regular rests
        dotted notes
        dotted rests
"""
from pprint         import pprint

from music21_globals  import SCORE_DATAPATH
from music21_globals  import unpickle_it

REG_NOTES = ['Whole Note', 'Half Note', 'Quarter Note', 'Eighth Note', 'Sixteenth Note']
REG_RESTS = ['Whole Rest', 'Half Rest', 'Quarter Rest', 'Eighth Rest', 'Sixteenth Rest']
DOT_NOTES = ['Dotted Whole Note', 'Dotted Half Note', 'Dotted Quarter Note', 'Dotted Eighth Note', 'Dotted Sixteenth Note']
DOT_RESTS = ['Dotted Whole Rest', 'Dotted Half Rest', 'Dotted Quarter Rest', 'Dotted Eighth Rest', 'Dotted Sixteenth Rest']


def find_rhythmatician_candidates(reg_notes=None, reg_rests=None, dot_notes=None, dot_rests=None, num_items=None):
    # Step 1: Retrieve data 
    score_dictionary = unpickle_it(pickle_path=SCORE_DATAPATH, be_verbose=False)
    # pprint(score_dictionary)

    # Step 2: Build query
    # search_list = []
    # if reg_notes:
    #     for next_item in REG_NOTES:
    #         search_list.append(next_item)
    # if reg_rests:
    #     for next_item in REG_RESTS:
    #         search_list.append(next_item)
    # if dot_notes:
    #     for next_item in DOT_NOTES:
    #         search_list.append(next_item)
    # if dot_rests:
    #     for next_item in DOT_RESTS:
    #         search_list.append(next_item)
    # pprint(search_list)
    
    # Step 3: Initial search. Eliminate all titles with too many types of notes/rests.
    # pprint(score_dictionary['can can']['Rhythm']['Values']['Types'])
    
    first_pass_list =[]
    
    for next_title in score_dictionary:
        if len(score_dictionary[next_title]['Rhythm']['Values']['Types']) == num_items and next_title not in first_pass_list:
            first_pass_list.append(next_title)
            
    for next_entry in first_pass_list:
        print(f"{next_entry}: {score_dictionary[next_entry]['Rhythm']['Values']['Types']} \n")
        
    # pprint(first_pass_list)
    
    
    # hit_list = []
    # for next_title in score_dictionary:
    #     for next_type in score_dictionary[next_title]['Rhythm']['Values']['Types']:
    #         if next_type in search_list:
    #             if next_title not in hit_list:
    #                 hit_list.append(next_title)
    #             else:
    #                 continue
    # pprint(f"{hit_list}")
    
    
    
if __name__ == '__main__':
    find_rhythmatician_candidates(reg_notes=True, reg_rests=True, dot_notes=False, dot_rests=False, num_items=2)
    
    # Program does not know the difference between notes and rests / regular and dotted.
    # What about tuplets?