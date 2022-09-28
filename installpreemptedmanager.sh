#!/bin/bash
# scale_up_endpoint="https://vmss-scaler.azurewebsites.net/api/httpscaleuptrigger"
preempted_event_manager=/srv/preemptedeventmanager/check-preemt-events.sh
touch $preempted_event_manager

printf 'REQ=$(curl -H Metadata:true http://169.254.169.254/metadata/scheduledevents?api-version=2020-07-01)\n\n' >> $preempted_event_manager
printf 'if [[ $REQ == *"Preempt"* ]]; then\n' >> $preempted_event_manager
printf '    echo "PREEMT | EVICTED"\n' >> $preempted_event_manager
printf '    curl %s\n' $scale_up_endpoint >> $preempted_event_manager
printf 'fi\n' >> $preempted_event_manager

crontab -l > mycron
echo "* * * * * for i in {1..6}; do /bin/bash $preempted_event_manager & sleep 10; done" >> mycron
crontab mycron
rm mycron
