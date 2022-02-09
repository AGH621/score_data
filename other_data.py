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
    Figure out whether a score has repeats and what type they are.
    """
    for next_score in score_dictionary:
        parsed = score_dictionary[next_score]['File Information']['Stream']
        
        # Gives the true length of piece if all repeats are performed
        repeats = len(repeat.Expander(parsed.parts[0]).measureMap())
        
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
def chords(score_dictionary, my_metadata):
    """
    Return True if a score has chord symbols, False if not
    """
    pass



#
#-----------------------------------------------------------------------------------------------
def slurs(score_dictionary, my_metadata):
    """
    Return the number of slurs in a score and the lengths of each.
    """
    pass



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
    
    