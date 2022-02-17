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
def number_of_parts(score_dictionary, my_metadata):
    """
    Get how many parts a score has.
    """
    for next_score in score_dictionary:
        score_dictionary[next_score]['Other'] = {}
        parsed = score_dictionary[next_score]['File Information']['Stream']
        
        num_parts = len(parsed.parts)
        
        score_dictionary[next_score]['Other'].update({'Parts': num_parts})

    #pprint(score_dictionary)
    return score_dictionary

#
#-----------------------------------------------------------------------------------------------
def measure_length(score_dictionary, my_metadata):
    """
    Get how many measures a score has printed.  Repeats are NOT included in this tally.
    """
    for next_score in score_dictionary:
        parsed = score_dictionary[next_score]['File Information']['Stream']

        m_length = len(parsed.parts[0].getElementsByClass(stream.Measure))
        #print(f"{next_score}: {m_length}")
        
        score_dictionary[next_score]['Other'].update({'Length': m_length})

    #pprint(score_dictionary)
    return score_dictionary
#
#-----------------------------------------------------------------------------------------------
def repeats(score_dictionary, my_metadata):
    """
    Figure out whether a score has repeats.
    
    Can use [score].recurse().spanners to locate ending repeats:
        la bamba: <music21.spanner.RepeatBracket 1 <music21.stream.Measure 22 offset=42.0><music21.stream.Measure 23 offset=44.0>>
        la bamba: <music21.spanner.RepeatBracket 2 <music21.stream.Measure 24 offset=46.0>>
    """
    for next_score in score_dictionary:
        parsed = score_dictionary[next_score]['File Information']['Stream']
        
        # Gives the true length of piece if all repeats are performed
        #repeats = len(repeat.Expander(parsed.parts[0]).measureMap())
        
        repeats = parsed.parts[0].recurse().getElementsByClass(repeat.RepeatMark)
        for next_thing in repeats:
            print(f"{next_score}: {next_thing} - {len(repeats)}")
        
        # The number of printed measures in the score if no repeats were performed
        s_length = score_dictionary[next_score]['Other']['Length']
        
        if repeats == s_length:
            score_dictionary[next_score]['Other'].update({'Repeats': False})
        
        else:
            score_dictionary[next_score]['Other'].update({'Repeats': True})

    #pprint(score_dictionary)
    return score_dictionary

#
#-----------------------------------------------------------------------------------------------
def form(score_dictionary, my_metadata):
    """
    Figure out the form of a piece.  NOTE: This may not be possible.
    """
    raise NotImplementedError ("Unknown how to determine using Music21")

#
#-----------------------------------------------------------------------------------------------
def lyrics(score_dictionary, my_metadata):
    """
    Extract the lyrics from each score.
    """
    for next_score in score_dictionary:
        parsed = score_dictionary[next_score]['File Information']['Stream']
        
        s_lyrics = text.assembleLyrics(parsed)    
        
        if s_lyrics:
            score_dictionary[next_score]['Other']['Lyrics'] = s_lyrics
        else:
            score_dictionary[next_score]['Other']['Lyrics'] = None

    #pprint(score_dictionary)
    return score_dictionary

#
#-----------------------------------------------------------------------------------------------
def chords_symbols(score_dictionary, my_metadata):
    """
    Find scores with chord symbols using Music21.  Iterate through scores with chords and list all the chord symbols in each part.  
    Count the number of each specific chord.
    
    Returns (as a part of the Score Dictionary):
        1) Complete list of all chords for each part.
        2) A set of unique chords with its number of occurances.
        3) If there are no chords the dictionary entries are None.
    """
    # Parse each score and set up the dictionary to store the data
    for next_score in score_dictionary:
        parsed = score_dictionary[next_score]['File Information']['Stream']
        score_dictionary[next_score]['Other']['Chords'] = {'All': {}}
        
        # Iterate through each part and extract the chord symbols
        for i, next_part in enumerate(parsed.parts):
            part_chords = next_part.recurse().getElementsByClass(harmony.ChordSymbol)

            # Collect chords into a list
            if part_chords:
                chord_list = []
                for next_chord in part_chords:
                    chord_list.append(next_chord.figure)
                
                # Add the list(s) to the dictionary
                score_dictionary[next_score]['Other']['Chords']['All'].update({'Part '+ str(i+1): chord_list})
                
                # Create a list of chords in all parts to identify and count chord appearances
                symbol_list = []
                for next_part in score_dictionary[next_score]['Other']['Chords']['All']:
                    for next_symbol in score_dictionary[next_score]['Other']['Chords']['All'][next_part]:
                        symbol_list.append(next_symbol)
                
                # Set up the dictionary for unique chord types
                score_dictionary[next_score]['Other']['Chords'].update({'Types': {}})

                # Count the number of each unique chord type and add it.
                for next_chord in set(symbol_list):
                    chord_count = 0
                    for next_sym in symbol_list:
                        if next_chord == next_sym:
                            chord_count += 1
                    score_dictionary[next_score]['Other']['Chords']['Types'].update({next_chord: chord_count})
                
            # If there are no chord symbols, set dictionary values to None
            else:
                score_dictionary[next_score]['Other']['Chords']['All'].update({'Part '+ str(i+1): None})
                score_dictionary[next_score]['Other']['Chords'].update({'Types': None})

    return score_dictionary

#
#-----------------------------------------------------------------------------------------------
def slurs(score_dictionary, my_metadata):
    """
    Return the number of slurs in a score and the lengths of each.
    """
    for next_score in score_dictionary:
        parsed = score_dictionary[next_score]['File Information']['Stream']
        score_dictionary[next_score]['Other']['Slurs'] = {}
        
        slur_count = 0
        slur_length = []
        
        #for i, next_part in enumerate(parsed.parts):
            #part_slur = next_part.recurse().spanners
            #print(f"{next_score}: {part_slur}")
        
        #for slur in parsed.recurse().spanners:
            #print(f"{next_score}: {slur}")

        for el in parsed.recurse().getElementsByClass(spanner.Slur):
            #print(f"{next_score}: {el.getSpannedElements()}") 
            slur_count +=1
            
            if len(el) not in slur_length:
                slur_length.append(len(el))
            
        #print(f"{next_score}: {slur_count} - {slur_length}")

        if slur_count != 0:
            score_dictionary[next_score]['Other']['Slurs']['Number'] = slur_count
            score_dictionary[next_score]['Other']['Slurs']['Lengths'] = slur_length
            
        else:
            score_dictionary[next_score]['Other']['Slurs']['Number'] = None
            score_dictionary[next_score]['Other']['Slurs']['Lengths'] = None
            
    #pprint(score_dictionary)
    return score_dictionary

#                                           MAIN
#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':

    # Retreive the Score Dictionary and metadata.
    score_dictionary = unpickle_it(pickle_path=SCORE_DATAPATH, be_verbose=False)
    my_metadata = access_metadata()
    
    number_of_parts(score_dictionary, my_metadata)
    measure_length(score_dictionary, my_metadata)
    repeats(score_dictionary, my_metadata)
    lyrics(score_dictionary, my_metadata)
    chords_symbols(score_dictionary, my_metadata)
    slurs(score_dictionary, my_metadata)
    
    #pprint(score_dictionary)
    #pickle_it(score_dictionary, pickle_path=SCORE_DATAPATH, text_path=SCORE_LOGPATH)
    
    