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
    with io.open(filepath, 'r') as f:
        return json.load(f)

def singleSprintStory():
    return _load_json('single_sprint_story.json')
    
def multiSprintStory():
    return _load_json('multi_sprint_story.json')

def negativeHistoryStory():
    return _load_json('neg_history_story.json')

def noSprintStory():
    return _load_json('no_sprint_story.json')

def zeroPointStory():
    return _load_json('zero_point_story.json')

def acceptedStory():
    return _load_json('accepted_story.json')

def doneWithNoProgress():
    return _load_json('done_with_no_progress.json')
    
def simpleBug():
    return _load_json('simple_bug.json')

def nested_data():
    return _load_json('nested_data.json')

