# Jira Reporting Scripts (0.99.10)

To address some of the deficiencies in Jira reporting, here is a small command line tool to 
exercise the [Jira REST API](https://docs.atlassian.com/jira/REST/cloud/) to retrieve information about Stories,
including story points and iterations and export into CSV format. This enables building better reports in Excel.

Notes: 0.99.8 has been refactored to make use of generators for improved efficiency
 and significantly cleaned up the codebase. Also, csv content is now only ASCII text.

MacOS:   Python 2.7 & 3.6 (tested)
Windows: Python 3.6 (tested), 2.7 (not tested)

## New Features

### OS credential storage

Added the `keyring` module, enabling storage of your Jira credentials in your OSes keychain or credential vault. MacOS and Windows are supported. The script may prompt that Python wants to access `qjira-sp` in your credential store. You should allow it always, unless you really like typing your password over and over again.

### JQL query

Added the `jql` command, print output of any provided JQL query.

### Technical Debt

Added the `debt` command, prints a table of story points versus bug points including percentage of tech debt (bugs) completed per project.

### Bug Backlog

Added the bug `backlog` command, prints all bugs by fix version.

# Commands

```
usage: qjira [-h] [-d] {cycletime,velocity,summary,debt,backlog,jql} ...

Export data from Jira to CSV format

optional arguments:
  -h, --help            show this help message and exit
  -d                    Debug level

Available commands:
  {cycletime,velocity,summary,debt,backlog,jql}
                        Available commands to process data
    cycletime           Produce cycletime data
    velocity            Produce velocity data
    summary             Produce summary report
    debt                Produce tech debt report
    backlog             Query bug backlog by fixVersion
    jql                 Query using JQL
```

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

# Future enhancements

  *  Add field and count_field arguments to JQL command

  *  Add argument including set of default IIQ project names 

  *  Unify sprint names & date ranges

# Installation

  * Uses setuptools for installation. On MacOS, install requires root permission via `sudo`. 

`$ pip install git+https://github.com/andrew-hamlin-sp/jira_reporting_scripts.git`

# Command line usage

  * View help message
  
`$ qjira -h`
`$ qjira {command} -h`

  * Produce velocity data
  
`$ qjira velocity -f 7.2 IIQHH`
  
  * Produce cycletime data
  
`$ qjira cycletime -f 7.2 IIQCB`

  * Produce summary report

`$ qjira summary -f 7.2 IIQCB`

  * Produce technical debt report
  
`$ qjira debt -f 7.2 IIQCB`

  * Produce bug backlog listing
  
`$ qjira backlog -f 7.3 IIQETN`

  * Multiple projects and output CSV file
  
`$ qjira velocity IIQCB IIQHH -o velocity.csv`

# Dependencies

  * requests
  
  * python-dateutil
  
  * keyring
  
  * six

# Development

Use python virtualenv to isolate the required libraries. `$ source bin/activate`

Update dependencies, `$ make init`

Clean build tree, `$ make clean`

Package distribution, `$ make dist` or `$ make dist-all`

Run all tests, `$ make test`

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

  
