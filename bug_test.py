#!/usr/bin/env python3
from music21            import *
from music21_globals    import *
from pprint             import pprint

the_metadata = metadata.bundles.MetadataBundle('scoreLibrary')
the_metadata.read()

envir = environment.UserSettings()
print(environment.UserSettings())
print(environment.UserSettings().getSettingsPath())

# for x in range(len(the_metadata)):
#     print(f'{the_metadata[x].metadata.sourcePath} - {the_metadata[x].metadata.pitchLowest}')
#
# score_dictionary = unpickle_it(pickle_path=SCORE_DATAPATH, be_verbose=False)
# pprint(score_dictionary)
#
# for next_score in score_dictionary:
#     s = corpus.manager.parse(score_dictionary[next_score]['File Information']['Path'])
#     p = analysis.discrete.Ambitus()
#     print(f'{next_score}{p.getSolution(s)}')
#     test = s.recurse().getElementsByClass(note.GeneralNote)
#     print(test)

# -------------------------------- Minor Solfeg Test Box -----------------------------------------
#


# Test Scores:
#     '/Users/AnneH/Dropbox (Personal)/Score Library/xml_all_clean/william he had seven sons.musicxml'
#     '/Users/AnneH/Dropbox (Personal)/Score Library/xml_all_clean/bim bom.musicxml'
#     '/Users/AnneH/Dropbox (Personal)/Score Library/xml_all_clean/head shoulders baby.musicxml'

# Parse the score:
# s = corpus.manager.parse('/Users/AnneH/Dropbox (Personal)/Score Library/xml_all_clean/william he had seven sons.musicxml')
# test = analysis.discrete.Ambitus().getSolution(s)
# print(test)
#
# dMin = key.Key('d')
# print("Pitch('F')",  dMin.solfeg(pitch.Pitch('F'), variant='music21'))       #   'mi'
# print("Pitch('F')",  dMin.solfeg(pitch.Pitch('F'), variant='humdrum'))       #   'mi'
# print("Pitch('A')",  dMin.solfeg('A', chromatic=True))                                              #   'fi'
# print("Pitch('A')",  dMin.solfeg('A', chromatic=False))                             #   'fa'
# print("Pitch('G#')", dMin.solfeg(pitch.Pitch('G#'), variant='music21'))     # default 'mis'
# print("Pitch('G#')", dMin.solfeg(pitch.Pitch('G#'), variant='humdrum'))     #    'my'
#
#
# dMinor = scale.MinorScale('d')
#
# print(dMinor.solfeg(pitch.Pitch('f-')))
# print(dMinor.getPitches())

#dflatMajor.solfeg(pitch.Pitch('E'))


#dflatMajor.solfeg(pitch.Pitch('E#'))

