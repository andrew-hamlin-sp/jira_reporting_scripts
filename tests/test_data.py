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
        ]
    },
    'changelog':{
        'histories':[
            {
                'created':'2017-01-30T11:56:10.061-0600',
                'items':[
                    {
                        'field':'status',
                        'to':'3'
                    }
                ]
            },
            {
                'created':'2017-01-31T11:56:10.061-0600',
                'items':[
                    {
                        'field':'status',
                        'to':'10001'
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
        'customfield_10016': None
    }
}

STORY_NO_POINTS={
    'key':123,
    'fields':{
        'customfield_10109': None,
        'customfield_10016': [
            SPRINT2
        ]
    }
}

STORY_NO_DATES={
    'key':123,
    'fields':{
        'customfield_10109': 5.0,
        'customfield_10016': [
            SPRINT3
        ]
    }
}

