#!/bin/bash
eval "$(jq -r '@sh "url=\(.url) filter=\(.filter) counter=\(.counter) sleep=\(.sleep) prefix=\(.prefix) password=\(.password)"')"
initial=$counter
timeout=true
echo $url > /tmp/ssh_keepalive_$prefix.vars
echo $filter >> /tmp/ssh_keepalive_$prefix.vars
echo $counter >> /tmp/ssh_keepalive_$prefix.vars
echo $sleep >> /tmp/ssh_keepalive_$prefix.vars 
echo $password >> /tmp/ssh_keepalive_$prefix.vars 
rm /tmp/ssh_keepalive_$prefix.out 2&> /dev/null
until [[ ! -z $(sshpass -p $password ssh -o LogLevel=quiet -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@$url hostname > /tmp/ssh_keepalive_$prefix.out && cat /tmp/ssh_keepalive_$prefix.out | grep "$filter" | wc -l) || $counter -lt 0 ]]; do
    let counter--
    sleep $sleep
done
secs=$((initial - counter))
secs=$((secs*sleep))
if [ $counter -ne -1 ]; then
   timeout=false
fi
jq -n --arg seconds "$secs" --arg is_timeout "$timeout" '{"seconds_to_deploy":$seconds, "timeout":$is_timeout}' '.[]'