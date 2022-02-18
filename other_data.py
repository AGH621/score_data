#!/usr/bin/env python3
"""
Song Search Other Data
written by: Anne Hamill
created on: 4 February 2022

Populate the other dictionary for each score in this format:

    { Other:
        { Parts:    number,
          Length:   in measures,
          Repeats:  boolean,     # for now -- not sure how to figure out the type    
          Form:     type,        # not possible right now
          Lyrics:   list,
          Chords:   boolean      # ???
          Slurs:    number and length  
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
def number_of_parts(a_dictionary, score):
    """
    Get how many parts a score has.
    """

    parsed = a_dictionary[score]['File Information']['Stream']
    num_parts = len(parsed.parts)
    a_dictionary[score]['Other'].update({'Parts': num_parts})
    
    return a_dictionary

#
#-----------------------------------------------------------------------------------------------
def measure_length(a_dictionary, score):
    """
    Get how many measures a score has printed.  Repeats are NOT included in this tally.
    """
    
    parsed = a_dictionary[score]['File Information']['Stream']
    m_length = len(parsed.parts[0].getElementsByClass(stream.Measure))
    a_dictionary[score]['Other'].update({'Length': m_length})
    
    return a_dictionary
    
#
#-----------------------------------------------------------------------------------------------
def repeats(a_dictionary, score):
    """
    If a score has repeats return the type of repeats.  If it does not return None.
    
    TODO: 
        1) What if a score has both a text repeat and a repeat sign?
        2) What about scores with bracket endings?  How does Music21 handle them?
    """

    parsed = a_dictionary[score]['File Information']['Stream']
    
    # Gives the true length of piece if all repeats are performed
    text_repeats = parsed.parts[0].recurse().getElementsByClass(repeat.RepeatExpression)
    bar_repeats = parsed.parts[0].recurse().getElementsByClass(bar.Repeat)
    
    if text_repeats:
        for next_text in text_repeats:
            if next_text.name != 'fine' or next_text.name != 'coda':
                a_dictionary[score]['Other'].update({'Repeats': next_text.name})
    
    elif bar_repeats:
        for next_bar in bar_repeats:
            a_dictionary[score]['Other'].update({'Repeats': 'repeat sign'})
    
    else:
        a_dictionary[score]['Other'].update({'Repeats': None})

    return a_dictionary

#
#-----------------------------------------------------------------------------------------------
def form(a_dictionary, score):
    """
    Figure out the form of a piece.  NOTE: This may not be possible.
    """
    raise NotImplementedError ("Unknown how to determine using Music21")

#
#-----------------------------------------------------------------------------------------------
def lyrics(a_dictionary, score):
    """
    Extract the lyrics from each score and assemble them into words.
    
    Returns the first verse worth of lyrics.  Returns None if it is an instrumental score.
    """

    parsed = a_dictionary[score]['File Information']['Stream']
    s_lyrics = text.assembleLyrics(parsed)    
    
    if s_lyrics:
        a_dictionary[score]['Other']['Lyrics'] = s_lyrics
    else:
        a_dictionary[score]['Other']['Lyrics'] = None

    return a_dictionary

#
#-----------------------------------------------------------------------------------------------
def chords_symbols(a_dictionary, score):
    """
    Find scores with chord symbols using Music21.  Iterate through scores with chords and list all the chord symbols in each part.  
    Count the number of each specific chord.
    
    Returns (as a part of the Score Dictionary):
        1) Complete list of all chords for each part.
        2) A set of unique chords with its number of occurances.
        3) If there are no chords the dictionary entries are None.
    """
    # Parse each score and set up the dictionary to store the data
    
    parsed = a_dictionary[score]['File Information']['Stream']
    a_dictionary[score]['Other']['Chords'] = {'All': {}}
    
    # Iterate through each part and extract the chord symbols
    for i, next_part in enumerate(parsed.parts):
        part_chords = next_part.recurse().getElementsByClass(harmony.ChordSymbol)

        # Collect chords into a list
        if part_chords:
            chord_list = []
            for next_chord in part_chords:
                chord_list.append(next_chord.figure)
            
            # Add the list(s) to the dictionary
            a_dictionary[score]['Other']['Chords']['All'].update({'Part '+ str(i+1): chord_list})
            
            # Create a list of chords in all parts to identify and count chord appearances
            symbol_list = []
            for next_part in a_dictionary[score]['Other']['Chords']['All']:
                for next_symbol in a_dictionary[score]['Other']['Chords']['All'][next_part]:
                    symbol_list.append(next_symbol)
            
            # Set up the dictionary for unique chord types
            a_dictionary[score]['Other']['Chords'].update({'Types': {}})

            # Count the number of each unique chord type and add it.
            for next_chord in set(symbol_list):
                chord_count = 0
                for next_sym in symbol_list:
                    if next_chord == next_sym:
                        chord_count += 1
                a_dictionary[score]['Other']['Chords']['Types'].update({next_chord: chord_count})
            
        # If there are no chord symbols, set dictionary values to None
        else:
            a_dictionary[score]['Other']['Chords']['All'].update({'Part '+ str(i+1): None})
            a_dictionary[score]['Other']['Chords'].update({'Types': None})

    return a_dictionary

#
#-----------------------------------------------------------------------------------------------
def slurs(a_dictionary, score):
    """
    Return the number of slurs in a score and the lengths of each.
    """
    
    parsed = a_dictionary[score]['File Information']['Stream']
    a_dictionary[score]['Other']['Slurs'] = {}
    
    slur_count = 0
    slur_length = []

    for el in parsed.recurse().getElementsByClass(spanner.Slur):
        slur_count +=1
        
        if len(el) not in slur_length:
            slur_length.append(len(el))

    if slur_count != 0:
        a_dictionary[score]['Other']['Slurs']['Number'] = slur_count
        a_dictionary[score]['Other']['Slurs']['Lengths'] = slur_length
        
    else:
        a_dictionary[score]['Other']['Slurs']['Number'] = None
        a_dictionary[score]['Other']['Slurs']['Lengths'] = None

    return a_dictionary

#                                           MAIN
#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':

    # Retreive the Score Dictionary and metadata.
    score_dictionary = unpickle_it(pickle_path=SCORE_DATAPATH, be_verbose=False)
    my_metadata = access_metadata()
    
    #number_of_parts(score_dictionary, my_metadata)
    #measure_length(score_dictionary, my_metadata)
    repeats(score_dictionary, my_metadata)
    #lyrics(score_dictionary, my_metadata)
    #chords_symbols(score_dictionary, my_metadata)
    #slurs(score_dictionary, my_metadata)
    
    pprint(score_dictionary)
    #pickle_it(score_dictionary, pickle_path=SCORE_DATAPATH, text_path=SCORE_LOGPATH)
    
    