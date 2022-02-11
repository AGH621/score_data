#!/usr/bin/env python3
"""
Song Search Pitch Data
written by: Anne Hamill
created on: 1 February 2022

Populate the pitch dictionary for each score in this format:

    { Pitch:
        { Key Signature:    list,
          Mode:             derived from key signature,                              
          Clef:             list,
          Letter Names:     { All: list of letter names in order of appearance,
                              Types: list of unique letter:appearance dictionaries
                            },
          Solfege:          { All: list of solfege syllables in order of appearance,
                              Types: list of unique solfege:appearance dictionaries
                            },
          Intervals:        { All: list of intervals in order of appearance,
                              Types: list of intervals:appearance dictionaries
                            },
          Range:            highest note, lowest note, interval between them,        
          Slurs:            number and length
        }
"""
#                                           IMPORTS
#-----------------------------------------------------------------------------------------------

import re

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
def key_signature(score_dictionary, my_metadata):
    """
    Analyze the key of each piece in 3 different ways.  Return the key which the majority of methods agrees upon, or the most accurate method.
    (Which is not that accurate).
    
    NOTE: Because of the multiple analyses, this method does take measurable time.  Consider multiple processing methods.
    """
    for next_score in score_dictionary:
        score_dictionary[next_score]['Pitch'] = {}
        parsed = score_dictionary[next_score]['File Information']['Stream']
        
        for x in range(len(my_metadata)):
            if my_metadata[x].metadata.sourcePath == score_dictionary[next_score]['File Information']['Path']:
                if my_metadata[x].metadata.ambitus.semitones == 0:
                    score_dictionary[next_score]['Pitch']['Key Signature'] = 'Unpitched'
                    
                else:
                    tur_key = parsed.recurse().getElementsByClass(key.Key)[0]      # only returns major keys
                    mon_key = parsed.analyze('key.krumhanslschmuckler')
                    hoc_key = parsed.analyze('key')

                    if tur_key == mon_key:
                        real_key = tur_key
                    elif tur_key == hoc_key:
                        real_key = tur_key
                    elif mon_key == hoc_key:
                        real_key = mon_key
                    else:
                        real_key = tur_key
                        
                    score_dictionary[next_score]['Pitch'].update({'Key Signature': str(real_key)})   #needs str() to add a string
    
    #pprint(score_dictionary)
    return score_dictionary

#
#-----------------------------------------------------------------------------------------------
def clef(score_dictionary, my_metadata):
    """
    This funcation needs to iterate through every part.
    """
    for next_score in score_dictionary:
        score_dictionary[next_score]['Pitch']['Clef'] = []
        parsed = score_dictionary[next_score]['File Information']['Stream']
        
        for next_part in parsed.parts:
            raw_clef = next_part.recurse().getElementsByClass('Clef')[0]
            processing = str(raw_clef).split('.')[-1].strip('>')
            finish_clef = re.sub('([A-Z])', r' \1', processing).strip()
            
            if finish_clef not in score_dictionary[next_score]['Pitch']['Clef']:
                score_dictionary[next_score]['Pitch']['Clef'].append(finish_clef)

    #pprint(score_dictionary)
    return score_dictionary

#
#-----------------------------------------------------------------------------------------------
def melody_range(score_dictionary, my_metadata):
    """
    Get the interval range, lowest note, and highest note for each part from music21.alaysis.discrete module.
    """
    for next_score in score_dictionary:
        parsed = score_dictionary[next_score]['File Information']['Stream']
        score_dictionary[next_score]['Pitch']['Range'] = {}
        
        for x in range(len(parsed.parts)):
            if score_dictionary[next_score]['Pitch']['Key Signature'] != 'Unpitched': 
                step_1 = analysis.discrete.Ambitus()
                pitchMin, pitchMax = step_1.getPitchSpan(parsed.parts[x])
                score_dictionary[next_score]['Pitch']['Range'].update({'Part '+str(x+1): {}})
                score_dictionary[next_score]['Pitch']['Range']['Part '+str(x+1)].update({'Lowest Note': str(pitchMin)})
                score_dictionary[next_score]['Pitch']['Range']['Part '+str(x+1)].update({'Highest Note': str(pitchMax)})

                step_2 = step_1.getSolution(parsed.parts[x])
                step_3 = str(step_2).split('.')[-1].strip('Interval').strip('>')
                score_dictionary[next_score]['Pitch']['Range']['Part '+str(x+1)].update({'Interval': str(step_3)})
            else:
                score_dictionary[next_score]['Pitch']['Range'].update({'Part '+str(x+1): {}})
                score_dictionary[next_score]['Pitch']['Range']['Part '+str(x+1)].update({'Lowest Note': None})
                score_dictionary[next_score]['Pitch']['Range']['Part '+str(x+1)].update({'Highest Note': None})
                score_dictionary[next_score]['Pitch']['Range']['Part '+str(x+1)].update({'Interval': None})
            
    #pprint(score_dictionary)
    return score_dictionary
#
#-----------------------------------------------------------------------------------------------
def letter_names(score_dictionary, my_metadata):
    """
    Get the letter names for each part of each score.
    """
    # Parse the scores and set up the dictionaries.
    for next_score in score_dictionary:
        parsed = score_dictionary[next_score]['File Information']['Stream']
        score_dictionary[next_score]['Pitch']['Letter Names'] = {'All': {}}
        
        for i, next_part in enumerate(parsed.parts):
            
            # If a score is unpitched we fill in the dictionary entries with None.
            if score_dictionary[next_score]['Pitch']['Key Signature'] == 'Unpitched':
                score_dictionary[next_score]['Pitch']['Letter Names']['All'].update({'Part '+ str(i+1): None})
                score_dictionary[next_score]['Pitch']['Letter Names'].update({'Types': None})

            # Otherwise the score has pitches and needs processing.
            else:
                # List to store notes
                note_list = []
            
                # Recurse the part and get the Note attribute of the M21 note class.  
                score_notes = next_part.recurse().getElementsByClass(note.Note)
            
                # Iterate through the notes to extract the parts we need.
                for next_note in score_notes:
                
                    # We take the last character of the string
                    only_letter = str(next_note).split('.')[-1].split()[-1].strip('>')
                    note_list.append(only_letter)
                
                # Add list of letter names for each part to dictionary.
                score_dictionary[next_score]['Pitch']['Letter Names']['All'].update({'Part '+ str(i+1): note_list})

                # Create a list of all letters for counting appearances.
                letter_list = []
                for next_part in score_dictionary[next_score]['Pitch']['Letter Names']['All']:
                    for next_note in score_dictionary[next_score]['Pitch']['Letter Names']['All'][next_part]:
                        letter_list.append(next_note)

                # Set up dictionary for unique letter names
                score_dictionary[next_score]['Pitch']['Letter Names'].update({'Types': {}})

                # Count instances of each letter.  
                for next_note in set(letter_list):
                    note_count = 0
                    for next_letter in letter_list:
                        if next_note == next_letter:
                            note_count += 1

                    # Add letter and count to dictionary
                    score_dictionary[next_score]['Pitch']['Letter Names']['Types'].update({next_note: note_count})

    return score_dictionary
#
#-----------------------------------------------------------------------------------------------
def solfege_names(score_dictionary, my_metadata):
    """
    Get the solfege names for each part of each score.
    """
    # Parse the scores and set up the dictionaries
    for next_score in score_dictionary:
        parsed = score_dictionary[next_score]['File Information']['Stream']
        score_dictionary[next_score]['Pitch']['Solfege'] = {'All': {}}
        
        for i, next_part in enumerate(parsed.parts):
            
            # If a score is unpitched we fill in the dictionary entries with None
            if score_dictionary[next_score]['Pitch']['Key Signature'] == 'Unpitched':
                score_dictionary[next_score]['Pitch']['Solfege']['All'].update({'Part '+ str(i+1): None})
                score_dictionary[next_score]['Pitch']['Solfege'].update({'Types': None})
            
            # Pitched scores need to be processed
            else:
                # Create a Music21 key object to use for solfege calculation
                letter_key = score_dictionary[next_score]['Pitch']['Key Signature'].split()[0]
                m21_key = key.Key(letter_key)
                
                # Use Music21 solfege function calculate the syllables for each part of each score
                solfege_list = []
                for next_list in score_dictionary[next_score]['Pitch']['Letter Names']['All']:
                    
                    for next_note in score_dictionary[next_score]['Pitch']['Letter Names']['All'][next_list]:
                        sol_note = m21_key.solfeg(next_note)
                        solfege_list.append(sol_note)
                        
                score_dictionary[next_score]['Pitch']['Solfege']['All'].update({'Part '+ str(i+1): solfege_list})
                
                # Create a master syllable list for counting appearances
                total_sol = []
                for next_part in score_dictionary[next_score]['Pitch']['Solfege']['All']:
                    for next_note in score_dictionary[next_score]['Pitch']['Solfege']['All'][next_part]:
                        total_sol.append(next_note)

                # Set up dictionary for unique solfege syllables
                score_dictionary[next_score]['Pitch']['Solfege'].update({'Types': {}})

                # Count instances of each syllable  
                for next_note in set(total_sol):
                    sol_count = 0
                    for next_syll in total_sol:
                        if next_note == next_syll:
                            sol_count += 1

                    # Add syllable and count to dictionary
                    score_dictionary[next_score]['Pitch']['Solfege']['Types'].update({next_note: sol_count})

    return score_dictionary
#
#-----------------------------------------------------------------------------------------------
def intervals(score_dictionary, my_metadata):
    """
    Get the solfege names for each part of each score.
    """
    # Parse the scores and set up the dictionaries
    for next_score in score_dictionary:
        parsed = score_dictionary[next_score]['File Information']['Stream']
        score_dictionary[next_score]['Pitch']['Intervals'] = {'All': {}}
        
        for i, next_part in enumerate(parsed.parts):
            
            # If a score is unpitched we fill in the dictionary entries with None
            if score_dictionary[next_score]['Pitch']['Key Signature'] == 'Unpitched':
                score_dictionary[next_score]['Pitch']['Intervals']['All'].update({'Part '+ str(i+1): None})
                score_dictionary[next_score]['Pitch']['Intervals'].update({'Types': None})

            # Pitched scores need to be processed
            else:
                # List to store notes
                interval_list = []
            
                # Flatten the part and get the Note attribute of the Music21 note class.  
                our_notes = next_part.flat.getElementsByClass(note.Note)
                
                # Use Music21 to calculate the intervals (Unknown why this is part of the segmentByRests class)
                the_intervals = analysis.segmentByRests.Segmenter.getIntervalList(our_notes)
                
                # Make the list with friendly names and add it
                interval_list = [x.name for x in the_intervals]
                score_dictionary[next_score]['Pitch']['Intervals']['All'].update({'Part '+ str(i+1): interval_list})

                # Create a master interval list for counting appearances
                total_int = []
                for next_part in score_dictionary[next_score]['Pitch']['Intervals']['All']:
                    for next_int in score_dictionary[next_score]['Pitch']['Intervals']['All'][next_part]:
                        total_int.append(next_int)

                # Set up dictionary for unique intervals
                score_dictionary[next_score]['Pitch']['Intervals'].update({'Types': {}})

                # Count instances of each syllable  
                for next_int in set(total_int):
                    int_count = 0
                    for next_dis in total_int:
                        if next_int == next_dis:
                            int_count += 1

                    # Add syllable and count to dictionary
                    score_dictionary[next_score]['Pitch']['Intervals']['Types'].update({next_int: int_count})

    return score_dictionary

#                                           MAIN
#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    # Retreive the Score Dictionary and metadata.
    score_dictionary = unpickle_it(pickle_path=SCORE_DATAPATH, be_verbose=False)
    my_metadata = access_metadata()

    key_signature(score_dictionary, my_metadata)
    clef(score_dictionary, my_metadata)
    melody_range(score_dictionary, my_metadata)
    letter_names(score_dictionary, my_metadata)
    solfege_names(score_dictionary, my_metadata)
    intervals(score_dictionary, my_metadata)

    pprint(score_dictionary)
    pickle_it(score_dictionary, pickle_path=SCORE_DATAPATH, text_path=SCORE_LOGPATH)

