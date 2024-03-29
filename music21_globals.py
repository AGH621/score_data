#!/usr/bin/env python3
"""
Score Librarian
written by: Anne Hamill
created on: 23 October 2020
"""
#                                           IMPORTS
#-----------------------------------------------------------------------------------------------
from music21    import *
from pprint     import pprint
from pprint     import PrettyPrinter
from pathlib    import Path
from deepdiff   import DeepDiff 

import os
import time
import pickle
import inspect
import codecs

#                                           VARIABLES
#-----------------------------------------------------------------------------------------------

SCORE_DATAPATH           = Path.home().joinpath('Dropbox (Personal)', 'Score Library', 'score_search', 'score_data', '_Data', 'score_dictionary.pkl')
SCORE_LOGPATH            = Path.home().joinpath('Dropbox (Personal)', 'Score Library', 'score_search', 'score_data', '_Logs', 'score_dictionary.txt')
CORPUS_FILEPATH          = Path.home().joinpath('Dropbox (Personal)', 'Score Library', 'all_musicxml')
CACHE_FILEPATH           = Path.home().joinpath('Dropbox (Personal)', 'Score Library', 'score_search', 'score_data', '_cache')

#                                            METHODS
#-----------------------------------------------------------------------------------------------
def reset_corpus():
    """
    Delete the old local corpus when a new one becomes available.
    """
    old_corpus = corpus.corpora.LocalCorpus('scoreLibrary')
    old_corpus.delete()
    print(corpus.manager.listLocalCorporaNames())
#
#-----------------------------------------------------------------------------------------------
def define_corpus():
    """
    Define the local corpus for our searches.  
    Turn off logging print statements by changing verbose to False in corpora.py Line 190 & 193.
    
    TODO: Turn ofF the automatic metadata caching.
    """
    our_corpus = corpus.corpora.LocalCorpus('scoreLibrary')
    
    our_corpus.addPath(CORPUS_FILEPATH)

    our_corpus.save()
    print(corpus.manager.listLocalCorporaNames())
    
    return our_corpus
#
#-----------------------------------------------------------------------------------------------
def build_metadata_cache():
    """
    If there are changes in the score directory, will this method need to be run to make sure the cache data match the score data?
        Delete file = rebuild metadata cache
        Add file = rebuild metadata cache
        [Not necessary to rebuild corpus]
    
    Turn off logging print statements by changing verbose to False in corpora.py Line 190 & 193.
    """
    # This may be useful at some point.
    #cache_file = Path.joinpath(CACHE_FILEPATH, 'cache_test.json')
    #if cache_file in CACHE_FILEPATH.iterdir():
        #pass

    corpus.corpora.LocalCorpus('scoreLibrary').cacheFilePath = Path.joinpath(CACHE_FILEPATH, 'our_corpus_cache.json')
    corpus.corpora.LocalCorpus('scoreLibrary').rebuildMetadataCache()
#
#-----------------------------------------------------------------------------------------------
def access_metadata():
    """
    """
    the_metadata = metadata.bundles.MetadataBundle('scoreLibrary')
    the_metadata.read()
    return the_metadata
#
#-----------------------------------------------------------------------------------------------
def score_file_info():
    """
    Using Music21's metadata sourcePath, create a unique string for each file to be used as its key in the Score Dictionary.
    Add the full sourcePath to the dictionary.  Then look at the file itself and add the Content Created and Content Modified datetimes.
    
    NOTE: Created and Modified times vary by system.  Will need to put a timestamp in the file itself should this program ever be shared by users on separate machines.
    
    TODO:   1) Create and append Music21 streams to non-leadsheet scores?  [Not sure I want this.]
            2) Rethink created on and modified on.  Because musicxmls might be re-created with each edit, rather than modified.
        
    Tests:  1) What if file path does not exist?
            2) What if file is empty or corrupt?
            3) What if the file info is missing?  [Is this even possible?]
            4) What if the file info is corrupt?  [Is this even possible?]
    """
    # Step 1: Open the Score Dictionary.
    score_dictionary = {}

    # Step 2: Access the metadata for each score.  This means define the bundle and read it.
    my_metadata = access_metadata()

    # Step 3: Iterate through the bundle and extract the sourcePath. Split it until only the file name without extension and variants remain.  This is the key.
    sc_family = []
    for x in range(len(my_metadata)):
        score_path = my_metadata[x].metadata.sourcePath
        file_name = score_path.split('/')[-1].split('.')[0]
        
        
        if ' - ' not in file_name: 
            score_dictionary[file_name] = {'File Information': {}}
            score_dictionary[file_name]['File Information'].update({'Path': score_path})
            #score_dictionary[file_name]['File Information'].update({'Family': ['Lead Sheet']})
        
        else:
            sc_family.append({file_name: score_path})
            #if 'Family' in score_dictionary[file_name]['File Information'].keys():
                #print('ok')

    # Step 4: Add the variant scores.
    for x in range(len(sc_family)):
        for key in sc_family[x]:
            org_sc = key.split(' - ')
            if org_sc[0] in score_dictionary:
                if 'Family' not in score_dictionary[org_sc[0]]['File Information'].keys():
                    score_dictionary[org_sc[0]]['File Information'].update({'Family': {org_sc[-1].title(): sc_family[x][key]}})
                    
                else:
                    score_dictionary[org_sc[0]]['File Information']['Family'].update({org_sc[-1].title(): sc_family[x][key]})

    # Step 5: Iterate through each file in the Score Dictionary.
    for next_score in score_dictionary:
        next_path = Path(score_dictionary[next_score]['File Information']['Path'])
        
        # Retrieve the Create Time using st_birthtime (MacOS = ok, not sure about others), convert into human readable form, and add to Score Dictionary -> File Information.
        c_float_sec = next_path.stat().st_birthtime
        create_time = time.ctime(c_float_sec)
        score_dictionary[next_score]['File Information'].update({'Created On': create_time})

        # Repeat for Modified Time. [TODO: Iterate through os.stat() to process create and modified times simultaneously?]
        m_float_sec = next_path.stat().st_mtime
        modify_time = time.ctime(m_float_sec)
        score_dictionary[next_score]['File Information'].update({'Modified On': modify_time})
    
    # Step 6: Add the Music21 stream.
    for next_score in score_dictionary:
        parse_score = corpus.manager.parse(score_dictionary[next_score]['File Information']['Path'])
        score_dictionary[next_score]['File Information']['Stream'] = parse_score
    
    pickle_it(score_dictionary, pickle_path=SCORE_DATAPATH, text_path=SCORE_LOGPATH)
        
    return score_dictionary
#
#-----------------------------------------------------------------------------------------------
def pickle_it(a_structure, pickle_path=None, text_path=None):
    """
    Pickle a data structure.
    """
    try:
        # Pickle the materials dictionary
        with open(pickle_path, 'wb') as the_store:
            pickle.dump(a_structure, the_store)

        # Derive a text file from the pickle created in the previous step and do a formatted print
        with codecs.open(text_path, encoding='utf-8', mode='w') as ITPKL:
            report_pp = PrettyPrinter(indent=2, width=160, stream=ITPKL)
            print('The Pickled Data Structure:\n', file=ITPKL)
            report_pp.pprint(a_structure)

    # Attempt to figure out why pickling failed miserably.
    except IOError as why:
        caller_name = inspect.stack()[1][3]
        print(f'{caller_name}  trying to save "{pickle_path}"')
        print (f'  - saved_structure: Exception: {why}')
        raise
#
#-----------------------------------------------------------------------------------------------
def unpickle_it(pickle_path=None, be_verbose=False):
    """
    Unpickle a data structure.
    """
    try:
        # Retreive the materials_dictionary.
        with open(pickle_path, 'rb') as dict_store:
            materials_dict = pickle.load(dict_store)

            assert isinstance(materials_dict, dict)
            return materials_dict

    # If retreiving fails, attempt to let the user know what happened.
    except Exception as why:
        if be_verbose:
            caller_name = inspect.stack()[1][3]
            print(f'{caller_name}  trying to retrieve "{pickle_path}"')
            print (f'  - new_dict: Exception: {why}')
        raise
#
#-----------------------------------------------------------------------------------------------        
def update_metadata_cache():
    """
    Determine whether there have been changes in the corpus directory and if the metadata cache file needs updating. Save the old metadata cache as a backup.
    Need to do 2 checks:
        1) Have files been added or deleted?  Compare directory info with entry in Score Dictionary -> File Information -> Path
        2) Have files been modified?  Compare file info with entry in Score Dictionary -> File Information -> Modified On
    
    TODO: Need a more precise rebuild process. Instead of rebuilding the whole Score Dictionary, only add/delete/modify the entire Score Dictionary, 
          only change the entries that have been identified as different.
    """
    # Check 1: Have files been added or deleted? 
    # Step 1: Get the file paths from the xml directory and put them in a list.
    paths = Path(CORPUS_FILEPATH).glob('**/*.musicxml')
    files = [x for x in paths if x.is_file() and ' - ' not in str(x)]
    
    
    # Step 2: Extract the file paths from the Score Dictionary and put them in a list.
    score_dictionary = unpickle_it(pickle_path=SCORE_DATAPATH, be_verbose=False)
    score_list = []
    for next_score in score_dictionary:
        score_path = score_dictionary[next_score]['File Information']['Path']
        score_list.append(Path(score_path))


    # Step 3: Sort the lists.
    score_list.sort()
    files.sort()
    
    #print(f"Score List: {score_list}")
    
    #for next_path in files:
        #if next_path not in score_list:
            #print(f"File Path: {next_path}")
    
    # Step 4: Compare the lists.  If they are the same then the corpus has not changed, proceed to Check 2.   
    if score_list == files:
        print(">>>>> The score dictionary and the local corpus directory contain the same files. Proceeding to Step 2 of update analysis. <<<<<\n")
        
        # Check 2: Have any of the files been modified?
        # Step A: Retreive the mtime from the xml directory, translate to the form in the Score Dictionary, put in a dictionary.
        file_mod_time = {}
        for next_file in files:
            m_float_sec = next_file.stat().st_mtime
            file_time = time.ctime(m_float_sec)
            file_mod_time.update({str(next_file): file_time})
        
        #pprint(file_mod_time)

        # Step B: Retreive the "Modified On" time from the Score Dictionary, put in a dictionary.
        score_mod_time = {}
        for next_score in score_dictionary:
            score_time = score_dictionary[next_score]['File Information']['Modified On']
            score_mod_time.update({score_dictionary[next_score]['File Information']['Path']: score_time})
        
        #pprint(score_mod_time)

        # Step C: Use the deepdiff library to compare the 2 dictionaries
        diff = DeepDiff(score_mod_time, file_mod_time)
        
        #for next_entry in diff:
            #for x in range(len(diff[next_entry])):
                #print(f"{diff[next_entry][x]}\n")

        
        # Step D: If deepdiff returns a populated dictionary, then modifications have occurred.  Rebuild the metadata and Score Dictionary.
        if len(diff) > 0:
            print(">>>>> Files in the local corpus directory have been modified.  Rebuilding the music21 metadata cache and score dictionary. <<<<<")
            
            # Before rebuilding, change the name of the current cache file in case we need to walk it back.
            current_cache = Path.joinpath(CACHE_FILEPATH, 'our_corpus_cache.json')
            current_cache.rename(Path.joinpath(CACHE_FILEPATH, 'old_cache.json'))
            
            # Now rebuild
            build_metadata_cache()
            score_file_info()
        
        # If deepdiff returns an empty dictionary, then everything is the same and we're finished.
        else:
            print(">>>>> The local corpus directory and score dictionary match.  No action required.  Analysis finished. <<<<<")
            
    # The corpus has changed.  Rebuild the metadata and Score Dictionary.
    else:
        print(">>>>> The score dictionary and local corpus directory are different. Rebuilding the Music21 metadata cache and score dictionary. <<<<<\n")
        
        #Before rebuilding, change the name of the current cache file in case we need to walk it back.
        current_cache = Path.joinpath(CACHE_FILEPATH, 'our_corpus_cache.json')
        current_cache.rename(Path.joinpath(CACHE_FILEPATH, 'old_cache.json'))
        
        # Now rebuild
        build_metadata_cache()
        score_file_info()
        
#
#----------------------------------------------------------------------------------------------- 
def find_file(file_name, directory_name):
    files_found = []
    for path, subdirs, files in os.walk(directory_name):
        for name in files:
            if(file_name == name):
                file_path = os.path.join(path,name)
                files_found.append(file_path)
    return files_found     

#                                           MAIN
#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    reset_corpus()
    define_corpus()
    build_metadata_cache()

    score_dictionary = score_file_info()
    update_metadata_cache()

    score_dictionary = unpickle_it(pickle_path=SCORE_DATAPATH, be_verbose=False)
    pprint(score_dictionary)
    
