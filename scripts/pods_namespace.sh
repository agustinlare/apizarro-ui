#/bin/bash
NAMESPACE=${1}

oc delete pods -n $NAMESPACE all