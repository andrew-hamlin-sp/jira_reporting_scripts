'''Canned test data'''

from copy import deepcopy

def singleSprintStory():
    return deepcopy(__TEST_DATA_TABLE['STORY'])

def multiSprintStory():
    return deepcopy(__TEST_DATA_TABLE['STORY_MULTI_SPRINT'])

def negativeHistoryStory():
    return deepcopy(__TEST_DATA_TABLE['STORY_NEGATIVE_HISTORY'])

def noSprintStory():
    return deepcopy(__TEST_DATA_TABLE['STORY_NO_SPRINT'])

def zeroPointStory():
    return deepcopy(__TEST_DATA_TABLE['STORY_NO_POINTS'])

def acceptedStory():
    return deepcopy(__TEST_DATA_TABLE['STORY_ACCEPTED'])

def doneWithNoProgress():
    return deepcopy(__TEST_DATA_TABLE['STORY_DONE_NO_PROGRESS'])


__SPRINT1 = 'com.atlassian.greenhopper.service.sprint.Sprint@be7f5f[id=82,rapidViewId=52,state=CLOSED,name=Chambers Sprint 9,goal=<null>,startDate=2016-04-25T10:44:22.273-05:00,endDate=2016-05-09T10:44:00.000-05:00,completeDate=2016-05-09T10:48:04.212-05:00,sequence=82]'

__SPRINT2 = 'com.atlassian.greenhopper.service.sprint.Sprint@be7f4e[id=83,rapidViewId=53,state=CLOSED,name=Chambers Sprint 10,goal=<null>,startDate=2016-05-10T10:44:22.27-05:00,endDate=2016-05-19T10:44:00.000-05:00,completeDate=2016-05-19T10:48:04.212-05:00,sequence=83]'

__SPRINT3 = 'com.atlassian.greenhopper.service.sprint.Sprint@be7f4e[id=83,rapidViewId=53,state=CLOSED,name=Sprint No Dates,goal=<null>,startDate=<null>,endDate=<null>,completeDate=<null>,sequence=83]'

__TEST_DATA_TABLE = {

    'STORY':{
        'key':123,
        'fields':{
            'customfield_10109': 3.0,
            'customfield_10016':[
                __SPRINT1
            ],
            'issuetype':{
                'name':'Story',
            },
            'project':{
                'key': 'Test'
            },
            'status':{
                'name':'Done'
            }
        },
        'changelog':{
            'histories':[
                {
                    'created':'2017-01-30T11:56:10.061-0600',
                    'items':[
                        {
                            'field':'status',
                            'fieldId':'status',
                            'to':'3',
                            'toString': 'In Progress'
                        }
                    ]
                },
                {
                    'created':'2017-01-31T11:56:10.061-0600',
                    'items':[
                        {
                            'field':'status',
                            'fieldId':'status',
                            'to':'10001',
                            'toString': 'Done'
                        }
                    ]
                }
            ]
        }
    },

    'STORY_MULTI_SPRINT':{
        'key':123,
        'fields':{
            'customfield_10109': 3.0,
            'customfield_10016':[
                __SPRINT2,
                __SPRINT1
            ],
            'issuetype':{
                'name':'Story',
            },
            'project':{
                'key': 'Test'
            },
            'status':{
                'name':'Done'
            }
        },
        'changelog':{
           'histories':[
               {
                   'created':'2017-01-30T11:56:10.061-0600',
                   'items':[
                       {
                           'field':'status',
                           'fieldId':'status',
                           'to':'3',
                           'toString': 'In Progress'
                       }
                   ]
               },
               {
                   'created':'2017-01-31T11:56:10.061-0600',
                   'items':[
                       {
                           'field':'status',
                           'fieldId':'status',
                           'to':'10001',
                           'toString': 'Done'
                       }
                   ]
               }
           ]
       }
    },


    'STORY_NO_SPRINT':{
        'key':123,
        'fields':{
            'customfield_10109': 3.0,
            'customfield_10016': None,
            'project':{
                'key': 'Test'
            },
            'status':{
                'name':'Done'
            }
        }
    },

    'STORY_NO_POINTS':{
        'key':123,
        'fields':{
            'customfield_10109': None,
            'customfield_10016': [
                __SPRINT2
            ],
            'project':{
                'key': 'Test'
            },
            'status':{
                'name':'Accepted'
            }
        }
    },

    'STORY_NO_DATES':{
        'key':123,
        'fields':{
            'customfield_10109': 5.0,
            'customfield_10016': [
                __SPRINT3
            ],
            'project':{
                'key': 'Test'
            },
            'status':{
                'name':'Open'
            }
        }
    },

    'STORY_NEGATIVE_HISTORY':{
        'key':123,
        'fields':{
            'customfield_10109': 3.0,
            'customfield_10016':[
                __SPRINT1
            ],
            'issuetype':{
                'name':'Story',
            },
            'project':{
                'key': 'Test'
            },
            'status':{
                'name':'Done'
            }
        },
        'changelog':{
            'histories':[
                {
                    'created':'2017-01-20T11:56:10.061-0600',
                    'items':[
                        {
                            'field':'status',
                            'fieldId':'status',
                            'to':'10001',
                            'toString': 'Done'
                        }
                    ]
                },
                {
                    'created':'2017-01-30T11:56:10.061-0600',
                    'items':[
                        {
                            'field':'status',
                            'fieldId':'status',
                            'to':'3',
                            'toString': 'In Progress'
                        }
                    ]
                },
                {
                    'created':'2017-01-31T11:56:10.061-0600',
                    'items':[
                        {
                            'field':'status',
                            'fieldId':'status',
                            'to':'10001',
                            'toString': 'Done'
                        }
                    ]
                }
            ]
        }
    },

    'STORY_ACCEPTED':{
        'key':123,
        'fields':{
            'customfield_10109': 3.0,
            'customfield_10016':[
                __SPRINT1
            ],
            'issuetype':{
                'name':'Story',
            },
            'project':{
                'key': 'Test'
            },
            'status':{
                'name':'Done'
            }
        },
        'changelog':{
            'histories':[
                {
                    'created':'2017-01-30T11:56:10.061-0600',
                    'items':[
                        {
                            'field':'status',
                            'fieldId':'status',
                            'to':'3',
                            'toString': 'In Progress'
                        }
                    ]
                },
                {
                    'created':'2017-01-31T11:56:10.061-0600',
                    'items':[
                        {
                            'field':'status',
                            'fieldId':'status',
                            'to':'10001',
                            'toString': 'Done'
                        }
                    ]
                },
                {
                    'created':'2017-02-03T11:56:10.061-0600',
                    'items':[
                        {
                            'field':'status',
                            'fieldId':'status',
                            'to':'10110',
                            'toString': 'Accepted'
                        }
                    ]
                },

            ]
        }
    },

    
    'STORY_DONE_NO_PROGRESS':{
        'key':123,
        'fields':{
            'customfield_10109': 3.0,
            'customfield_10016':[
                __SPRINT1
            ],
            'issuetype':{
                'name':'Story',
            },
            'project':{
                'key': 'Test'
            },
            'status':{
                'name':'Done'
            }
        },
        'changelog':{
            'histories':[
                {
                    'created':'2017-01-31T11:56:10.061-0600',
                    'items':[
                        {
                            'field': 'Link',
                            'fieldtype':'jira',
                            'to':'IIQCB-123',
                            'toString':'This is a link type without a fieldId causing cycletime bug'
                        },
                        {
                            'fieldId':'status',
                            'field':'status',
                            'to':'10001',
                            'toString': 'Done'
                        }
                    ]
                },
                {
                    'created':'2017-02-03T11:56:10.061-0600',
                    'items':[
                        {
                            'fieldId':'status',
                            'field':'status',
                            'to':'10110',
                            'toString': 'Accepted'
                        }
                    ]
                },

            ]
        }
    },
}

        
