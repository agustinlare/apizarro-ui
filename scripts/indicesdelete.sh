#!/bin/bash
pods=$(oc get pods --selector component=elasticsearch -o name|head -n 1)
es='es_util --query=app-000001 -XDELETE','es_util --query=infra-000001 -XDELETE'
for e in $es; do
    oc exec $pods -n openshift-logging -- ${e}
done