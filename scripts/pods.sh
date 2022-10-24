#/bin/bash
ARGS=${1}

namespace="echo $ARGS | awk '{print $1}'"
pods="echo $ARGS | awk '{print $2}'"

echo oc get pods -n $namespace $pods