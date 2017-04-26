# Jira Reporting Scripts

To address some of the deficiencies in Jira reporting, here is a small command line tool to 
exercise the [Jira REST API](https://docs.atlassian.com/jira/REST/cloud/) to retrieve information about Stories,
including story points and iterations and export into CSV format. This enables building better reports in Excel.

*Future enhancements*

  * Add option to exclude carry-over points from story points (default includes them)
  * Add option to include Bugs along with Stories (to include tech debt items)
  * Add summary command to show backlog summaries (Open stories plus details)
  * Use CSV module rather than brute force write()

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

  
