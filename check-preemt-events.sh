REQ=$(curl -H Metadata:true http://169.254.169.254/metadata/scheduledevents?api-version=2020-07-01)

if [[ $REQ == *"Preempt"* ]]; then
  echo "PREEMT | EVICTED"
#   curl 
fi
