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

def simpleBug():
    return deepcopy(__TEST_DATA_TABLE['BUG_SIMPLE'])


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
                'key': 'Test',
                'name': 'Test',
            },
            'status':{
                'name':'Done'
            },
            'customfield_14300': 'https://harbor.sailpoint.com/docs/DOC-20236',
            'customfield_11101': 'https://harbor.sailpoint.com/docs/DOC-19296'
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
                    'id': '291542',
                    'created': '2017-06-21T14:08:51.388-0500',
                    'items': [
                        {
                            'field': 'ENG Test Plan',
                            'fieldId': 'customfield_14300',
                            'fieldtype': 'custom',
                            'from': None,
                            'fromString': None,
                            'to': None,
                            'toString': 'https://harbor.sailpoint.com/docs/DOC-20236'
                        }
                    ]
                },
                {
                    'id': '291545',
                    'created': '2017-06-21T14:11:54.987-0500',
                    'items': [
                        {
                            'field': 'ENG Design',
                            'fieldId': 'customfield_11101',
                            'fieldtype': 'custom',
                            'from': None,
                            'fromString': None,
                            'to': None,
                            'toString': 'https://harbor.sailpoint.com/docs/DOC-19296'
                        }
                    ]
                },
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
            'customfield_10017':'test-1234',
            'issuetype':{
                'name':'Story',
            },
            'project':{
                'key': 'Test',
                'name': 'Test'
            },
            'status':{
                'name':'Done'
            },
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
                'key': 'Test',
                'name': 'Test'
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
                'key': 'Test',
                'name': 'Test'
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
                'key': 'Test',
                'name': 'Test'
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
                'key': 'Test',
                'name': 'Test'
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
                'key': 'Test',
                'name': 'Test'
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
                'key': 'Test',
                'name': 'Test'
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

    'BUG_SIMPLE':    {
      'key': 'IIQCB-1222',
      'changelog': {
        'startAt': 0,
        'maxResults': 10,
        'total': 10,
        'histories': [
          {
            'id': '336508',
            'created': '2017-06-27T09:33:23.571-0500',
            'items': [
              {
                'field': 'status',
                'fieldId': 'status',
                'fieldtype': 'jira',
                'from': '1',
                'fromString': 'Open',
                'to': '3',
                'toString': 'In Progress'
              }
            ]
          },
          {
            'id': '336975',
            'created': '2017-06-27T14:51:36.640-0500',
            'items': [
              {
                'field': 'Fixed In',
                'fieldId': 'customfield_10201',
                'fieldtype': 'custom',
                'from': '',
                'fromString': '',
                'to': '[15600]',
                'toString': '7.2'
              },
              {
                'field': 'status',
                'fieldId': 'status',
                'fieldtype': 'jira',
                'from': '3',
                'fromString': 'In Progress',
                'to': '10900',
                'toString': 'Need Review'
              }
            ]
          },
          {
            'id': '338414',
            'created': '2017-06-28T13:12:34.280-0500',
            'items': [
              {
                'field': 'resolution',
                'fieldId': 'resolution',
                'fieldtype': 'jira',
                'from': '',
                'fromString': '',
                'to': '10000',
                'toString': 'Done'
              },
              {
                'field': 'status',
                'fieldId': 'status',
                'fieldtype': 'jira',
                'from': '10900',
                'fromString': 'Need Review',
                'to': '5',
                'toString': 'Resolved'
              }
            ]
          },
          {
            'id': '338415',
            'created': '2017-06-28T13:12:43.471-0500',
            'items': [
              {
                'field': 'Story Points',
                'fieldId': 'customfield_10109',
                'fieldtype': 'custom',
                'from': '',
                'fromString': '1',
                'to': '',
                'toString': '3'
              }
            ]
          },
          {
            'id': '339489',
            'created': '2017-06-29T11:38:50.886-0500',
            'items': [
              {
                'field': 'Verified In',
                'fieldId': 'customfield_10202',
                'fieldtype': 'custom',
                'from': '',
                'fromString': '',
                'to': '[15600]',
                'toString': '7.2'
              },
              {
                'field': 'status',
                'fieldId': 'status',
                'fieldtype': 'jira',
                'from': '5',
                'fromString': 'Resolved',
                'to': '6',
                'toString': 'Closed'
              }
            ]
          }
        ]
      },
      'fields': {
        'customfield_10016': [
          'com.atlassian.greenhopper.service.sprint.Sprint@b16770[id=330,rapidViewId=52,state=CLOSED,name=IIQCB 7.2 Cycle 2 - 7,goal=,startDate=2017-06-19T10:54:03.982-05:00,endDate=2017-07-01T01:53:00.000-05:00,completeDate=2017-07-05T10:00:16.558-05:00,sequence=330]'
        ],
        'summary': 'Change warning dialog from blue header to yellow header',
        'customfield_10017': '',
        'issuetype': {
          'self': 'https://sailpoint.atlassian.net/rest/api/2/issuetype/10102',
          'id': '10102',
          'description': '',
          'iconUrl': 'https://sailpoint.atlassian.net/secure/viewavatar?size=xsmall&avatarId=10303&avatarType=issuetype',
          'name': 'Bug',
          'subtask': False,
        },
        'customfield_10109': 3.0,
        'customfield_14300': '',
        'project': {
          'self': 'https://sailpoint.atlassian.net/rest/api/2/project/11100',
          'id': '11100',
          'key': 'IIQCB',
          'name': 'Test Two',
        },
        'assignee': {
          'self': 'https://sailpoint.atlassian.net/rest/api/2/user?username=gauri.dhond',
          'name': 'gauri.dhond',
          'key': 'gauri.dhond',
          'accountId': '557058:063d20e9-5f17-471c-84fa-f69810d89632',
          'emailAddress': 'gauri.dhond@sailpoint.com',
          'displayName': 'Gauri Dhond',
          'active': True,
          'timeZone': 'America/Chicago'
        },
        'fixVersions': [
          {
            'self': 'https://sailpoint.atlassian.net/rest/api/2/version/15600',
            'id': '15600',
            'description': '',
            'name': '7.2',
            'archived': False,
            'released': False
          }
        ],
      }
    },
}

        
