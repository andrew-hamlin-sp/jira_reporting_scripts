# -*- coding: utf-8 -*-
"""Canned test data"""

import os
import io
import json

# load json test data
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

def _load_json(filename):
    filepath = os.path.join(dir_path, filename)
    print(filepath)
    with io.open(filepath, 'r') as f:
        return json.load(f)

def singleSprintStory():
    #return deepcopy(__TEST_DATA_TABLE['STORY'])
    return _load_json('single_sprint_story.json')
    
def multiSprintStory():
    #return deepcopy(__TEST_DATA_TABLE['STORY_MULTI_SPRINT'])
    return _load_json('multi_sprint_story.json')

def negativeHistoryStory():
    #return deepcopy(__TEST_DATA_TABLE['STORY_NEGATIVE_HISTORY'])
    return _load_json('neg_history_story.json')

def noSprintStory():
    #return deepcopy(__TEST_DATA_TABLE['STORY_NO_SPRINT'])
    return _load_json('no_sprint_story.json')

def zeroPointStory():
    #return deepcopy(__TEST_DATA_TABLE['STORY_NO_POINTS'])
    return _load_json('zero_point_story.json')

def acceptedStory():
    #return deepcopy(__TEST_DATA_TABLE['STORY_ACCEPTED'])
    return _load_json('accepted_story.json')

def doneWithNoProgress():
    #return deepcopy(__TEST_DATA_TABLE['STORY_DONE_NO_PROGRESS'])
    return _load_json('done_with_no_progress.json')
    
def simpleBug():
    #return deepcopy(__TEST_DATA_TABLE['BUG_SIMPLE'])
    return _load_json('simple_bug.json')

def nested_data():
    #return deepcopy(__TEST_DATA_TABLE['NESTED_DATA'])
    return _load_json('nested_data.json')

