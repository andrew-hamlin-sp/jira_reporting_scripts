# Run through set of commands against live Jira data
set -o errexit

echo -n ENTER JIRA PASSWORD:
read -s jpwd
echo

run_cmd() {
    qjira -w "$jpwd" --delimiter=$'\t' "$@"
}

echo "--begin summary test--"
run_cmd summary -f 7.3 IIQCB IIQMAG
echo "--end summary test--"

echo "--begin cycletime test--"
run_cmd cycletime -f 7.2 IIQCB IIQMAG
echo "--end cycletime test--"

echo "--begin velocity test--"
run_cmd velocity -f 7.2 IIQCB IIQMAG
echo "--end velocity test--"

echo "--begin debt test--"
run_cmd debt -f 7.3 IIQCB IIQMAG
echo "--end debt test--"

echo "--begin backlog test--"
run_cmd backlog -f 7.3 IIQCB IIQMAG
echo "--end backlog test--"

echo "--begin jql test--"
run_cmd jql 'project in projectsLeadByUser() AND fixVersion in unreleasedVersions() AND issuetype = Story AND status = Open'
echo "--end jql test--"

echo "--begin velocity forecast test--"
run_cmd velocity -f 7.3 -F IIQCB IIQMAG
echo "--end velocity forecast test--"
