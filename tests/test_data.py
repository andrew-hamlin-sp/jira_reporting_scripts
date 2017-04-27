'''Canned test data'''

SPRINT1='com.atlassian.greenhopper.service.sprint.Sprint@be7f5f[id=82,rapidViewId=52,state=CLOSED,name=Chambers Sprint 9,goal=<null>,startDate=2016-04-25T10:44:22.273-05:00,endDate=2016-05-09T10:44:00.000-05:00,completeDate=2016-05-09T10:48:04.212-05:00,sequence=82]'

SPRINT2='com.atlassian.greenhopper.service.sprint.Sprint@be7f4e[id=83,rapidViewId=53,state=CLOSED,name=Chambers Sprint 10,goal=<null>,startDate=2016-04-25T10:44:22.273-05:00,endDate=2016-05-09T10:44:00.000-05:00,completeDate=2016-05-09T10:48:04.212-05:00,sequence=83]'

SPRINT3='com.atlassian.greenhopper.service.sprint.Sprint@be7f4e[id=83,rapidViewId=53,state=CLOSED,name=Sprint No Dates,goal=<null>,startDate=<null>,endDate=<null>,completeDate=<null>,sequence=83]'

STORY={
    'key':123,
    'fields':{
        'customfield_10109': 3.0,
        'customfield_10016':[
            SPRINT1
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
                        'to':'10001',
                        'toString': 'Done'
                    }
                ]
            }
        ]
    }
}

STORY_NO_SPRINT={
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
}

STORY_NO_POINTS={
    'key':123,
    'fields':{
        'customfield_10109': None,
        'customfield_10016': [
            SPRINT2
        ],
        'project':{
            'key': 'Test'
        },
        'status':{
            'name':'Accepted'
        }
    }
}

STORY_NO_DATES={
    'key':123,
    'fields':{
        'customfield_10109': 5.0,
        'customfield_10016': [
            SPRINT3
        ],
        'project':{
            'key': 'Test'
        },
        'status':{
            'name':'Open'
        }
    }
}

BUG={
    "expand": "operations,versionedRepresentations,editmeta,changelog,renderedFields",
    "id": "44873",
    "self": "https://sailpoint.atlassian.net/rest/api/2/issue/44873",
    "key": "IIQCB-668",
    "changelog": {
        "startAt": 0,
        "maxResults": 9,
        "total": 9,
        "histories": [
            {
                "id": "94930",
                "author": {
                    "self": "https://sailpoint.atlassian.net/rest/api/2/user?username=marc.schulz",
                    "name": "marc.schulz",
                    "key": "marc.schulz",
                    "emailAddress": "marc.schulz@sailpoint.com",
                    "avatarUrls": {
                        "48x48": "https://sailpoint.atlassian.net/secure/useravatar?ownerId=marc.schulz&avatarId=11160",
                        "24x24": "https://sailpoint.atlassian.net/secure/useravatar?size=small&ownerId=marc.schulz&avatarId=11160",
                        "16x16": "https://sailpoint.atlassian.net/secure/useravatar?size=xsmall&ownerId=marc.schulz&avatarId=11160",
                        "32x32": "https://sailpoint.atlassian.net/secure/useravatar?size=medium&ownerId=marc.schulz&avatarId=11160"
                    },
                    "displayName": "Marc Schulz",
                    "active": True,
                    "timeZone": "America/Chicago"
                },
                "created": "2016-10-03T13:54:59.165-0500",
                "items": [
                    {
                        "field": "Fix Version",
                        "fieldtype": "jira",
                        "from": "11364",
                        "fromString": "7.1",
                        "to": None,
                        "toString": None
                    },
                    {
                        "field": "Fix Version",
                        "fieldtype": "jira",
                        "from": None,
                        "fromString": None,
                        "to": "13200",
                        "toString": "7.2"
                    }
                ]
            },
            {
                "id": "151063",
                "author": {
                    "self": "https://sailpoint.atlassian.net/rest/api/2/user?username=patrick.jeong",
                    "name": "patrick.jeong",
                    "key": "patrick.jeong",
                    "emailAddress": "patrick.jeong@sailpoint.com",
                    "avatarUrls": {
                        "48x48": "https://secure.gravatar.com/avatar/f2041f6ad7e6480be0dc475bc88610c4?d=mm&s=48",
                        "24x24": "https://secure.gravatar.com/avatar/f2041f6ad7e6480be0dc475bc88610c4?d=mm&s=24",
                        "16x16": "https://secure.gravatar.com/avatar/f2041f6ad7e6480be0dc475bc88610c4?d=mm&s=16",
                        "32x32": "https://secure.gravatar.com/avatar/f2041f6ad7e6480be0dc475bc88610c4?d=mm&s=32"
                    },
                    "displayName": "Patrick Jeong",
                    "active": True,
                    "timeZone": "America/Chicago"
                },
                "created": "2016-12-13T09:38:48.265-0600",
                "items": [
                    {
                        "field": "status",
                        "fieldtype": "jira",
                        "from": "1",
                        "fromString": "Open",
                        "to": "3",
                        "toString": "In Progress"
                    }
                ]
            },
            {
                "id": "151064",
                "author": {
                    "self": "https://sailpoint.atlassian.net/rest/api/2/user?username=patrick.jeong",
                    "name": "patrick.jeong",
                    "key": "patrick.jeong",
                    "emailAddress": "patrick.jeong@sailpoint.com",
                    "avatarUrls": {
                        "48x48": "https://secure.gravatar.com/avatar/f2041f6ad7e6480be0dc475bc88610c4?d=mm&s=48",
                        "24x24": "https://secure.gravatar.com/avatar/f2041f6ad7e6480be0dc475bc88610c4?d=mm&s=24",
                        "16x16": "https://secure.gravatar.com/avatar/f2041f6ad7e6480be0dc475bc88610c4?d=mm&s=16",
                        "32x32": "https://secure.gravatar.com/avatar/f2041f6ad7e6480be0dc475bc88610c4?d=mm&s=32"
                    },
                    "displayName": "Patrick Jeong",
                    "active": True,
                    "timeZone": "America/Chicago"
                },
                "created": "2016-12-13T09:38:59.671-0600",
                "items": [
                    {
                        "field": "Fixed In",
                        "fieldtype": "custom",
                        "from": None,
                        "fromString": None,
                        "to": "[13200]",
                        "toString": "7.2"
                    },
                    {
                        "field": "status",
                        "fieldtype": "jira",
                        "from": "3",
                        "fromString": "In Progress",
                        "to": "10900",
                        "toString": "Need Review"
                    }
                ]
            },
            {
                "id": "164588",
                "author": {
                    "self": "https://sailpoint.atlassian.net/rest/api/2/user?username=patrick.jeong",
                    "name": "patrick.jeong",
                    "key": "patrick.jeong",
                    "emailAddress": "patrick.jeong@sailpoint.com",
                    "avatarUrls": {
                        "48x48": "https://secure.gravatar.com/avatar/f2041f6ad7e6480be0dc475bc88610c4?d=mm&s=48",
                        "24x24": "https://secure.gravatar.com/avatar/f2041f6ad7e6480be0dc475bc88610c4?d=mm&s=24",
                        "16x16": "https://secure.gravatar.com/avatar/f2041f6ad7e6480be0dc475bc88610c4?d=mm&s=16",
                        "32x32": "https://secure.gravatar.com/avatar/f2041f6ad7e6480be0dc475bc88610c4?d=mm&s=32"
                    },
                    "displayName": "Patrick Jeong",
                    "active": True,
                    "timeZone": "America/Chicago"
                },
                "created": "2017-01-09T14:45:14.265-0600",
                "items": [
                    {
                        "field": "status",
                        "fieldtype": "jira",
                        "from": "10900",
                        "fromString": "Need Review",
                        "to": "5",
                        "toString": "Resolved"
                    },
                    {
                        "field": "resolution",
                        "fieldtype": "jira",
                        "from": None,
                        "fromString": None,
                        "to": "10000",
                        "toString": "Done"
                    }
                ]
            },
            {
                "id": "166686",
                "author": {
                    "self": "https://sailpoint.atlassian.net/rest/api/2/user?username=Sabrina.Kassamali",
                    "name": "Sabrina.Kassamali",
                    "key": "sabrina",
                    "emailAddress": "sabrina.kassamali@sailpoint.com",
                    "avatarUrls": {
                        "48x48": "https://sailpoint.atlassian.net/secure/useravatar?ownerId=sabrina&avatarId=11408",
                        "24x24": "https://sailpoint.atlassian.net/secure/useravatar?size=small&ownerId=sabrina&avatarId=11408",
                        "16x16": "https://sailpoint.atlassian.net/secure/useravatar?size=xsmall&ownerId=sabrina&avatarId=11408",
                        "32x32": "https://sailpoint.atlassian.net/secure/useravatar?size=medium&ownerId=sabrina&avatarId=11408"
                    },
                    "displayName": "Sabrina Kassamali",
                    "active": True,
                    "timeZone": "America/Chicago"
                },
                "created": "2017-01-11T10:53:24.340-0600",
                "items": [
                    {
                        "field": "QA Contact",
                        "fieldtype": "custom",
                        "from": "eric.lacey",
                        "fromString": "Eric Lacey",
                        "to": "sabrina",
                        "toString": "Sabrina Kassamali"
                    }
                ]
            },
            {
                "id": "166811",
                "author": {
                    "self": "https://sailpoint.atlassian.net/rest/api/2/user?username=Sabrina.Kassamali",
                    "name": "Sabrina.Kassamali",
                    "key": "sabrina",
                    "emailAddress": "sabrina.kassamali@sailpoint.com",
                    "avatarUrls": {
                        "48x48": "https://sailpoint.atlassian.net/secure/useravatar?ownerId=sabrina&avatarId=11408",
                        "24x24": "https://sailpoint.atlassian.net/secure/useravatar?size=small&ownerId=sabrina&avatarId=11408",
                        "16x16": "https://sailpoint.atlassian.net/secure/useravatar?size=xsmall&ownerId=sabrina&avatarId=11408",
                        "32x32": "https://sailpoint.atlassian.net/secure/useravatar?size=medium&ownerId=sabrina&avatarId=11408"
                    },
                    "displayName": "Sabrina Kassamali",
                    "active": True,
                    "timeZone": "America/Chicago"
                },
                "created": "2017-01-11T12:29:01.517-0600",
                "items": [
                    {
                        "field": "Verified In",
                        "fieldtype": "custom",
                        "from": None,
                        "fromString": None,
                        "to": "[13200]",
                        "toString": "7.2"
                    },
                    {
                        "field": "status",
                        "fieldtype": "jira",
                        "from": "5",
                        "fromString": "Resolved",
                        "to": "6",
                        "toString": "Closed"
                    }
                ]
            },
            {
                "id": "169079",
                "author": {
                    "self": "https://sailpoint.atlassian.net/rest/api/2/user?username=marc.schulz",
                    "name": "marc.schulz",
                    "key": "marc.schulz",
                    "emailAddress": "marc.schulz@sailpoint.com",
                    "avatarUrls": {
                        "48x48": "https://sailpoint.atlassian.net/secure/useravatar?ownerId=marc.schulz&avatarId=11160",
                        "24x24": "https://sailpoint.atlassian.net/secure/useravatar?size=small&ownerId=marc.schulz&avatarId=11160",
                        "16x16": "https://sailpoint.atlassian.net/secure/useravatar?size=xsmall&ownerId=marc.schulz&avatarId=11160",
                        "32x32": "https://sailpoint.atlassian.net/secure/useravatar?size=medium&ownerId=marc.schulz&avatarId=11160"
                    },
                    "displayName": "Marc Schulz",
                    "active": True,
                    "timeZone": "America/Chicago"
                },
                "created": "2017-01-13T16:04:04.491-0600",
                "items": [
                    {
                        "field": "Fixed In",
                        "fieldtype": "custom",
                        "from": "[13200]",
                        "fromString": "7.2",
                        "to": "[15600]",
                        "toString": "7.2"
                    },
                    {
                        "field": "Verified In",
                        "fieldtype": "custom",
                        "from": "[13200]",
                        "fromString": "7.2",
                        "to": "[15600]",
                        "toString": "7.2"
                    },
                    {
                        "field": "project",
                        "fieldtype": "jira",
                        "from": "11502",
                        "fromString": "IIQ - Bugs",
                        "to": "11100",
                        "toString": "IIQ - Chambers Bay"
                    },
                    {
                        "field": "Version",
                        "fieldtype": "jira",
                        "from": "11352",
                        "fromString": "6.4",
                        "to": None,
                        "toString": None
                    },
                    {
                        "field": "Version",
                        "fieldtype": "jira",
                        "from": None,
                        "fromString": None,
                        "to": "17596",
                        "toString": "6.4"
                    },
                    {
                        "field": "Fix Version",
                        "fieldtype": "jira",
                        "from": "13200",
                        "fromString": "7.2",
                        "to": None,
                        "toString": None
                    },
                    {
                        "field": "Fix Version",
                        "fieldtype": "jira",
                        "from": None,
                        "fromString": None,
                        "to": "15600",
                        "toString": "7.2"
                    },
                    {
                        "field": "Component",
                        "fieldtype": "jira",
                        "from": "11295",
                        "fromString": "UI",
                        "to": None,
                        "toString": None
                    },
                    {
                        "field": "Component",
                        "fieldtype": "jira",
                        "from": None,
                        "fromString": None,
                        "to": "11313",
                        "toString": "UI"
                    },
                    {
                        "field": "Key",
                        "fieldtype": "jira",
                        "from": None,
                        "fromString": "IIQETN-3147",
                        "to": None,
                        "toString": "IIQCB-668"
                    }
                ]
            },
            {
                "id": "169080",
                "author": {
                    "self": "https://sailpoint.atlassian.net/rest/api/2/user?username=marc.schulz",
                    "name": "marc.schulz",
                    "key": "marc.schulz",
                    "emailAddress": "marc.schulz@sailpoint.com",
                    "avatarUrls": {
                        "48x48": "https://sailpoint.atlassian.net/secure/useravatar?ownerId=marc.schulz&avatarId=11160",
                        "24x24": "https://sailpoint.atlassian.net/secure/useravatar?size=small&ownerId=marc.schulz&avatarId=11160",
                        "16x16": "https://sailpoint.atlassian.net/secure/useravatar?size=xsmall&ownerId=marc.schulz&avatarId=11160",
                        "32x32": "https://sailpoint.atlassian.net/secure/useravatar?size=medium&ownerId=marc.schulz&avatarId=11160"
                    },
                    "displayName": "Marc Schulz",
                    "active": True,
                    "timeZone": "America/Chicago"
                },
                "created": "2017-01-13T16:04:12.353-0600",
                "items": [
                    {
                        "field": "Story Points",
                        "fieldtype": "custom",
                        "from": None,
                        "fromString": None,
                        "to": None,
                        "toString": "1"
                    }
                ]
            },
            {
                "id": "169122",
                "author": {
                    "self": "https://sailpoint.atlassian.net/rest/api/2/user?username=marc.schulz",
                    "name": "marc.schulz",
                    "key": "marc.schulz",
                    "emailAddress": "marc.schulz@sailpoint.com",
                    "avatarUrls": {
                        "48x48": "https://sailpoint.atlassian.net/secure/useravatar?ownerId=marc.schulz&avatarId=11160",
                        "24x24": "https://sailpoint.atlassian.net/secure/useravatar?size=small&ownerId=marc.schulz&avatarId=11160",
                        "16x16": "https://sailpoint.atlassian.net/secure/useravatar?size=xsmall&ownerId=marc.schulz&avatarId=11160",
                        "32x32": "https://sailpoint.atlassian.net/secure/useravatar?size=medium&ownerId=marc.schulz&avatarId=11160"
                    },
                    "displayName": "Marc Schulz",
                    "active": True,
                    "timeZone": "America/Chicago"
                },
                "created": "2017-01-13T16:16:08.111-0600",
                "items": [
                    {
                        "field": "Sprint",
                        "fieldtype": "custom",
                        "from": None,
                        "fromString": None,
                        "to": "213",
                        "toString": "7.2 Cycle 1 - 1"
                    }
                ]
            }
        ]
    },
    "fields": {
        "customfield_10016": [
            "com.atlassian.greenhopper.service.sprint.Sprint@d80263[id=213,rapidViewId=52,state=CLOSED,name=7.2 Cycle 1 - 1,goal=,startDate=2017-01-03T21:08:14.387-06:00,endDate=2017-01-13T21:08:00.000-06:00,completeDate=2017-01-13T16:40:12.850-06:00,sequence=213]"
        ],
        "issuetype":{
            "name":"Bug",
        },
        "project": {
            "self": "https://sailpoint.atlassian.net/rest/api/2/project/11100",
            "id": "11100",
            "key": "IIQCB",
            "name": "IIQ - Chambers Bay",
            "avatarUrls": {
                "48x48": "https://sailpoint.atlassian.net/secure/projectavatar?avatarId=10324",
                "24x24": "https://sailpoint.atlassian.net/secure/projectavatar?size=small&avatarId=10324",
                "16x16": "https://sailpoint.atlassian.net/secure/projectavatar?size=xsmall&avatarId=10324",
                "32x32": "https://sailpoint.atlassian.net/secure/projectavatar?size=medium&avatarId=10324"
            }
        },
        "customfield_10109": 1.0
    }
}


STORY_NEGATIVE_HISTORY={
    'key':123,
    'fields':{
        'customfield_10109': 3.0,
        'customfield_10016':[
            SPRINT1
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
                        'to':'10001',
                        'toString': 'Done'
                    }
                ]
            }
        ]
    }
}
