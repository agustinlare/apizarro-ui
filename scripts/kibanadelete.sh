#!/bin/bash
USER=${1}
es_pod=$(oc get pods -o name -n openshift-logging -l component=elasticsearch | head -1)
for i in $(oc exec -c elasticsearch $es_pod -n openshift-logging -- es_util --query=_cat/indices -XGET|grep -i $USER | awk '{print $3}') ; do
   oc exec -c elasticsearch $es_pod -n openshift-logging -- es_util "--query=${i} -XDELETE"
done
