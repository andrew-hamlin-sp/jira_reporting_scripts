# Jira Reporting Scripts (0.99.4)

To address some of the deficiencies in Jira reporting, here is a small command line tool to 
exercise the [Jira REST API](https://docs.atlassian.com/jira/REST/cloud/) to retrieve information about Stories,
including story points and iterations and export into CSV format. This enables building better reports in Excel.

MacOS:   Python 2.7 & 3.6 (tested)
Windows: Python 3.6 (tested), 2.7 (not tested)

## New Features

### OS credential storage

Added the `keyring` module, enabling storage of your Jira credentials in your OSes keychain or credential vault. MacOS and Windows are supported. The script may prompt that Python wants to access `qjira-sp` in your credential store. You should allow it always, unless you really like typing your password over and over again.

### Tech Debt command

Added the tech debt `d` command, prints a table of story points versus bug points including percentage of tech debt (bugs) completed per project.

### Bug Backlog command

Added the bug backlog `b` command, prints all bugs by fix version.

## Summary

Prints backlog summary and documentation links for stories in a project using Excel formulas. Note: In order to
format correctly in a Harbor document import the CSV file into Excel using comma delimiters, then copy-paste the
table into your Harbor document.

## Velocity

Calculate the story points planned, completed, and carried over for every sprint associated with an issue.

Issues (story or bug) that have not been assigned at least one sprint will not be reported on (because velocity only makes sense in the context of a sprint(s).

Sprints without defined start and end dates will not be reported.

## Cycle Time

Calculate the days from being moved to In Progress by devs to being closed by testers.

Limitations: 

  * This does not subtract time for an issue moved from In Progress back to Open. 

  * This does not record separate values for bugs being dev complete 'Resolved' and being test complete 'Closed'.

## Tech Debt

Generate table of project_name, bug_points, story_points, & tech_debt percentage.

## Bug Backlog

Prints backlog summary of bugs by fix version. This adds a row per fix version for filtering in Excel.

## Future enhancements

  *  Enable Commands to extend the Jira field values

  *  Unify sprint names & date ranges

## Installation

  * Uses setuptools for installation. On MacOS, install requires root permission via `sudo`. 

`$ pip install git+https://github.com/andrew-hamlin-sp/jira_reporting_scripts.git`

## Command line usage

  * View help message
  
`$ qjira -h`
`$ qjira v -h`

  * Produce velocity data
  
`$ qjira v -p IIQHH`
  
  * Produce cycletime data
  
`$ qjira c -p IIQCB`

  * Produce summary report

`$ qjira s -p IIQCB`

  * Multiple projects and specific fix versions
  
`$ qjira v -p IIQCB -p IIQHH -F 7.2`

## Dependencies

  * requests
  * python-dateutil

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

  
