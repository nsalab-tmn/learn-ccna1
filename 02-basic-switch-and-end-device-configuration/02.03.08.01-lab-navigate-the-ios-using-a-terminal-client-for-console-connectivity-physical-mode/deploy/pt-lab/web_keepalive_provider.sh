#!/bin/bash
eval "$(jq -r '@sh "url=\(.url) filter=\(.filter) counter=\(.counter) sleep=\(.sleep) prefix=\(.prefix)"')"
initial=$counter
timeout=true
echo $url > /tmp/web_keepalive_$prefix.vars
echo $filter >> /tmp/web_keepalive_$prefix.vars
echo $counter >> /tmp/web_keepalive_$prefix.vars
echo $sleep >> /tmp/web_keepalive_$prefix.vars 
rm /tmp/web_keepalive_$prefix.out 2&> /dev/null
until [[ ! -z $(curl $url -k -s -L -I -o /tmp/web_keepalive_$prefix.out && cat /tmp/web_keepalive_$prefix.out | grep "$filter" | wc -l) || $counter -lt 0 ]]; do
    let counter--
    sleep $sleep
done
secs=$((initial - counter))
secs=$((secs*sleep))
if [ $counter -ne -1 ]; then
   timeout=false
fi
jq -n --arg seconds "$secs" --arg is_timeout "$timeout" '{"seconds_to_deploy":$seconds, "timeout":$is_timeout}' '.[]'