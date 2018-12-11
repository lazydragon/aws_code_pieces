# Background
AWS RDS monitoring already provides a few good metrics to monitor DB.

Yet there're some important metrics missing.

e.g.
connection status (used connection/max connection in percentage)
remaining disk space in percentage

# What is this script
This script helps you set up expressions on existing cloudwatch metrics and set up alarms for:
- connection status (used connection/max connection in percentage)
- remaining disk space in percentage

You can check these alarm status within AWS cloudwatch console.
You can also receive alerts via SMS/email.

# Restrictions
Currently we use AWS default max connection number in the metric calculation. If you set your customised max_connection in the parameter group, it is not supported by this script yet.

# Next step
command line this script, so you don't have to modify the code in order to use it.
