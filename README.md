# Jira Reporting Scripts

To address some of the deficiencies in Jira reporting, here is a small command line tool to 
exercise the [Jira REST API](https://docs.atlassian.com/jira/REST/cloud/) to retrieve information about Stories,
including story points and iterations and export into CSV format. This enables building better reports in Excel.


## Velocity

Calculate the story points planned, completed, and carried over for every sprint associated with an issue.

Issues (story or bug) that have not been assigned at least one sprint will not be reported on (because velocity only makes sense in the context of a sprint(s).

Sprints without defined start and end dates will not be reported.

## Cycle Time

Calculate the days from being moved to In Progress by devs to being Closed by testers.

Limitations: 

  * This does not subtract time for an issue moved from In Progress back to Open. 

  * This does not record separate values for bugs being dev complete 'Resolved' and being test complete 'Closed'.

*Future enhancements*

  * Add summary command to show backlog summaries (Open stories plus details)

## Dependencies

  * requests
  * python-dateutil

## Installation

  * Uses setuptools for installation

`$ pip install git+https://github.com/andrew-hamlin-sp/jira_reporting_scripts.git`

## Command line usage

  * View help message
  
`$ qjira -h`
`$ qjira v -h`

  * Produce velocity data
  
`$ qjira v -p IIQHH`
  
  * Produce cycletime data
  
`$ qjira c -p IIQCB`

## Development

Use python virtualenv to isolate the required libraries. `$ source bin/activate`

Update dependencies, `$ pip freeze > requirements.txt`

Run from development virtualenv, `$ python -mqjira -h`

Exit the virtualenv, `$ deactivate`

Basic make commands: 

*Run these from inside the virtualenv*

  * Initialize the project dependencies

`$ make init`

  * Run the unit tests

`$ make test`

  * Clean the binary and cached output
  
`$ make clean`

  
