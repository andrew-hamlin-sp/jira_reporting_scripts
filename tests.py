import unittest

from sprints import process_story_sprints, sprint_info

SPRINT1='com.atlassian.greenhopper.service.sprint.Sprint@be7f5f[id=82,rapidViewId=52,state=CLOSED,name=Chambers Sprint 9,goal=<null>,startDate=2016-04-25T10:44:22.273-05:00,endDate=2016-05-09T10:44:00.000-05:00,completeDate=2016-05-09T10:48:04.212-05:00,sequence=82]'

SPRINT2='com.atlassian.greenhopper.service.sprint.Sprint@be7f4e[id=83,rapidViewId=53,state=CLOSED,name=Chambers Sprint 10,goal=<null>,startDate=2016-04-25T10:44:22.273-05:00,endDate=2016-05-09T10:44:00.000-05:00,completeDate=2016-05-09T10:48:04.212-05:00,sequence=83]'

STORY={
    'key':123,
    'fields':{
        'customfield_10109': 3.0,
        'customfield_10016':[
            SPRINT1
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


class TestSprints(unittest.TestCase):

    def test_sprint_info(self):
        self.assertEqual({'name':'Chambers Sprint 9','id':'82','rapidViewId':'52','state':'CLOSED','goal':'<null>','startDate':'2016-04-25T10:44:22.273-05:00','endDate':'2016-05-09T10:44:00.000-05:00','completeDate':'2016-05-09T10:48:04.212-05:00','sequence':'82'}, sprint_info(SPRINT1))

    def test_process_story_sprints(self):
        r = next(process_story_sprints(STORY))
        self.assertTupleEqual(('Chambers Sprint 9', 123, 3.0), r)

    def test_process_story_sprints_NONE(self):
        r = next(process_story_sprints(STORY_NO_SPRINT))
        self.assertTupleEqual(('', 123, 3.0), r)

        
if __name__ == '__main__':
    unittest.main()
    
