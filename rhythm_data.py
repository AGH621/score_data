#!/usr/bin/env python3
"""
Song Search Rhythm Data
written by: Anne Hamill
created on: 9 January 2022
clean: 0

Populate the rhythm dictionary for each score in this format.

    { Rhythm:
        { Time Signature:      list,
          Meter:               calculated from time signature,
          Values:              { All:    {Part X: [list of note/rest values in order of appearance]},
                                 Types:  list of note:appearance dictionaries
                               },
          Ties                 { Number:  number
                                 Lengths:  list
                               },    
          Anacrusis:           quarterLength (music21-ism)                                      
        }
    }

"""
#                                           IMPORTS
#-----------------------------------------------------------------------------------------------
from music21        import *
from pprint         import pprint

from music21_globals  import SCORE_DATAPATH
from music21_globals  import SCORE_LOGPATH
from music21_globals  import unpickle_it
from music21_globals  import pickle_it
from music21_globals  import access_metadata
from music21_globals  import define_corpus

#                                            METHODS
#-----------------------------------------------------------------------------------------------
def time_signature(score_dictionary, my_metadata):
    """
    Extract the time signature information for each score and add to its dictionary.
    
    TODO: If a score has a hidden time signature, it cannot be extracted by music21, either through the metadata or 
    through getElementsByClass(meter.TimeSignature).  Is there a way to extrapolate the information from other properties?
    """
    
    # Add the rhythm sub-dictionary.
    for next_score in score_dictionary:
        score_dictionary[next_score]['Rhythm'] = {}
        
        # Try to get the time signatures out of the metadata.  If the time signature is hidden, this method will fail.
        for x in range(len(my_metadata)):
            if my_metadata[x].metadata.sourcePath == score_dictionary[next_score]['File Information']['Path']:
                if my_metadata[x].metadata.timeSignatures != []:
                    score_dictionary[next_score]['Rhythm'].update({'Time Signature': my_metadata[x].metadata.timeSignatures})
                else:
                    score_dictionary[next_score]['Rhythm'].update({'Time Signature': 'hidden'})

    return score_dictionary
#
#-----------------------------------------------------------------------------------------------
def meter(score_dictionary, my_metadata):
    """
    Using the time signature, figure out the score's meter.  We are working under the principle that there are three meters: duple, triple, and mixed.
    """
    # Figure out the meter based on the time signature.
    for next_score in score_dictionary:
        if score_dictionary[next_score]['Rhythm']['Time Signature'] != 'hidden':
            if len(score_dictionary[next_score]['Rhythm']['Time Signature']) == 1:
                top_num = score_dictionary[next_score]['Rhythm']['Time Signature'][0][0]
                if int(top_num) % 3 == 0:
                    score_dictionary[next_score]['Rhythm']['Meter'] = 'triple'
                else:
                    score_dictionary[next_score]['Rhythm']['Meter'] = 'duple'
            else:
                time_sigs = score_dictionary[next_score]['Rhythm']['Time Signature']
                m_list = []
                for n in range(len(time_sigs)):
                    top = time_sigs[n][0]
                    if int(top) % 3 == 0:
                        m_list.append('triple')
                    else:
                        m_list.append('duple')
                
                if len(set(m_list)) == 1:
                    score_dictionary[next_score]['Rhythm']['Meter'] = str(m_list)
                else:
                    score_dictionary[next_score]['Rhythm']['Meter'] = 'mixed'
        else:
            score_dictionary[next_score]['Rhythm']['Meter'] = 'unknown'
    
    #pprint(score_dictionary)
    return score_dictionary
#
#-----------------------------------------------------------------------------------------------
def value_list(score_dictionary, my_metadata):
    """
    Extract the note/rest value list from the leadsheet score and enter it into the score dictionary.
    Each part will need its own list.
    """
    # Parse each score from its stream.  Would like to break these two lines out into their own function, because it will be needs throughout the program
    for next_score in score_dictionary:    
        parsed = score_dictionary[next_score]['File Information']['Stream']
        
        # Add the All Values sub-dictionary to each score's data structure.
        #score_dictionary[next_score]['Rhythm']['Values'].update({'All': {}})
        score_dictionary[next_score]['Rhythm'].update({'Values': {'All': {}}})
        
        # Enumerate through the parsed parts because we need both the part and it's index number
        for i, next_part in enumerate(parsed.parts):
            
            # List to store notes
            note_list = []
            
            # Recurse the part and get the GeneralNote attribute of the M21 note class.  
            #General note is the only class attribute which accurately lists both notes and rests.
            score_notes = next_part.recurse().getElementsByClass(note.GeneralNote)
            
            # Iterate through the notes to extract the parts we need.
            for next_note in score_notes:
                
                # Notes we take the last two words of the string
                if next_note.fullName.endswith('Note'):
                    note_val = next_note.fullName.split()[4] + ' ' + next_note.fullName.split()[5]
                    note_list.append(note_val)
                
                # Rests we take the whole string. (We ignore chords in this function)   
                elif next_note.fullName.endswith('Rest'):
                    note_list.append(next_note.fullName)
                
            # Populate the sub-dictionary. Identify each part by its index number +1
            score_dictionary[next_score]['Rhythm']['Values']['All'].update({'Part '+ str(i+1): note_list})
            
            value_list = []
            for next_part in score_dictionary[next_score]['Rhythm']['Values']['All']:
                for next_note in score_dictionary[next_score]['Rhythm']['Values']['All'][next_part]:
                    value_list.append(next_note)
                
            #score_dictionary[next_score]['Rhythm']['Values'].update({'Types': list(set(value_list))})
        
            # Set up dictionary for unique letter names
            score_dictionary[next_score]['Rhythm']['Values'].update({'Types': {}})

            # Count instances of each letter.  
            for next_note in set(value_list):
                note_count = 0
                for next_value in value_list:
                    if next_note == next_value:
                        note_count += 1

                # Add letter and count to dictionary
                score_dictionary[next_score]['Rhythm']['Values']['Types'].update({next_note: note_count})
        
    #pprint(score_dictionary)
    return score_dictionary
#
#-----------------------------------------------------------------------------------------------
def value_types(score_dictionary, my_metadata):
    """
    Take the lists in the 'All Values' sub-dictionary and transform them into sets to eliminate duplicates.  
    This is the set of all the different note values in the piece.  Turn the set into a list and add as a separate sub-dictionary.
    
    TODO: Integrate this function into value_list()
    """
    for next_score in score_dictionary:
        value_list = []
        for next_part in score_dictionary[next_score]['Rhythm']['Values']['All']:
            for next_note in score_dictionary[next_score]['Rhythm']['Values']['All'][next_part]:
                value_list.append(next_note)
                
        #score_dictionary[next_score]['Rhythm']['Values'].update({'Types': list(set(value_list))})
        
        # Set up dictionary for unique letter names
        score_dictionary[next_score]['Rhythm']['Values'].update({'Types': {}})

        # Count instances of each letter.  
        for next_note in set(value_list):
            note_count = 0
            for next_value in value_list:
                if next_note == next_value:
                    note_count += 1

            # Add letter and count to dictionary
            score_dictionary[next_score]['Rhythm']['Values']['Types'].update({next_note: note_count})
    
    pprint(score_dictionary)
    return score_dictionary
#
#-----------------------------------------------------------------------------------------------
def anacrusis(score_dictionary, my_metadata):
    """
    Find out if a score has pick-up notes.  Count the number and type of notes used.  Record in Score Dictionary.
    """
    for next_score in score_dictionary:
        parsed = score_dictionary[next_score]['File Information']['Stream']
        
        try:
            pickup = repeat.RepeatFinder(parsed).getQuarterLengthOfPickupMeasure()
            score_dictionary[next_score]['Rhythm']['Anacrusis'] = pickup
        
        except repeat.InsufficientLengthException:
            score_dictionary[next_score]['Rhythm']['Anacrusis'] = 'not available'
    
    
    #pprint(score_dictionary)
    return score_dictionary
#
#-----------------------------------------------------------------------------------------------
def ties(score_dictionary, my_metadata):
    """
    Find out if a score has ties.  Count the number of ties and their length. Record all info in Score Dictionary.
    
    TODO: 1) Decide whether the note values in a tie are wanted.
    """
    for next_score in score_dictionary:
        parsed = score_dictionary[next_score]['File Information']['Stream']

        tie_count = 0
        lengths = []

        for n in range(len(parsed.recurse().notes)):
            note = parsed.recurse().notes[n]

            if note.tie:
                if note.tie.type == 'start':
                    tie_count +=1
                    tie_length = 2
                
                if note.tie.type == 'continue':
                    tie_length += 1
                
                if tie_length not in lengths:
                    lengths.append(tie_length)

        if lengths != []:
            #score_dictionary[next_score]['Rhythm']['Ties']['Lengths'] = lengths
            score_dictionary[next_score]['Rhythm'].update({'Ties': {'Lengths': lengths}})
        else:
            score_dictionary[next_score]['Rhythm'].update({'Ties': {'Lengths': None}})

        score_dictionary[next_score]['Rhythm']['Ties']['Number'] = tie_count

    return score_dictionary


#                                           MAIN
#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    # Retreive the Score Dictionary and metadata.
    score_dictionary = unpickle_it(pickle_path=SCORE_DATAPATH, be_verbose=False)
    my_metadata = access_metadata()
    
    time_signature(score_dictionary, my_metadata)
    meter(score_dictionary, my_metadata)
    value_list(score_dictionary, my_metadata)
    #value_types(score_dictionary, my_metadata)
    anacrusis(score_dictionary, my_metadata)
    ties(score_dictionary, my_metadata)

    pprint(score_dictionary)
    pickle_it(score_dictionary, pickle_path=SCORE_DATAPATH, text_path=SCORE_LOGPATH)
    
    