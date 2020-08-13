Dropmire
========

Dropmire is a flask application used by the Red Hat OSPO team to track points of contact for each community
we help. The system is based around an email workflow, where messages are sent on a regular basis to verify
that a point of contact is still valid. If no answer is heard, then it is automatically escalated to the manager and/or 
a super admin to fix the situation.

This is currently still a prototype and as such might never be finished. The deployment is done in OpenShift and can be completed by doing the following command:

`oc new-app dropmire-openshift/dropmire.yml -e MAIL_FROM=,<your-email>@redhat.com ADMINS=<admin-email>@<anywhere>.com`

After the deployment of this template file, you only need to expose the application with the following command:

`oc expose svc/dropmire`

And now, to see its route in openshift:

`oc get route`


Database backup and reinitialization
====================================

To back up the persistant volume of the database all you need to do is hit the `/download` endpoint, e.g.:

`<host.domain>/download`

This will offer you a CSV file named `data.csv` that contains all the current information in dropmires postgresql database. If you find yourself in need of redeploying dropmire and its persistent volume this file can be put in the migrations folder of a running dropmire container inside a live dropmire pod and, if you simply run the `db2csv.py` (without any arguments) from a bash shell, then it will initialize dropmire's postgresql database with all the information from inside the data.csv file.
