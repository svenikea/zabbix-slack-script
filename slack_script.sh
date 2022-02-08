#!/bin/bash

# Log all bash command to a file for debugging
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>>/tmp/output.log 2>&1


# Slack webhook url
slack_urls=() ## An array of slack webhook url!
# Username from which messages are coming from
username='Zabbix'

# Slack Alert information
## Slack user/channel ID with different recipient here!
unit_1_recipients=()
unit_2_recipients=() 
unit_3_recipients=() 
unit_4_recipients=() 
all_recipients="<!channel>" ## All user in the channel
time=$(date +"%Y.%m.%d %T")
zabbix_server_ip="192.168.1.3" ## This could be a domain name
channel="$1"
subject="$2"
message="$3"
status=$(echo ${message} | grep status | cut -d ">" -f10)
severity=$(echo ${message} | grep Severity | cut -d ">" -f4)
server=$(echo ${message} | grep Host | cut -d ">" -f2)
trigger_id=$(echo ${message} | grep triggerid | cut -d ">" -f12)
event_id=$(echo ${message} | grep eventid | cut -d ">" -f8)
op_data=$(echo ${message} | grep "opdata" | cut -d ">" -f6)
group=$(echo ${message} | grep "group" | cut -d ">" -f14)
link="http://${zabbix_server_ip}/zabbix/tr_events.php?triggerid=${trigger_id}&eventid=${event_id}"
colors=("#97AAB3" "#7499FF" "#FFC859" "#FFA059" "#E97659" "#E45959" "#009900") # Background color: No Information, Information, Warning, Black, High, Critical, Resolved  

# Set alert message type
if [[ $status == "OK" ]]; then
	type="R"
	title=":large_green_circle: Resolved: ${subject}"
elif [[ $status == "PROBLEM" ]]; then
	type="P"
	title=":red_circle: Problem: ${subject}"
else
	type="N"
fi

# Define alert recipient
if [[ $group == "matched group1" ]]; then
	if [[ $severity != "Disaster" ]]; then
		sendto="${unit_1_recipients}"
		slack_url=${slack_urls[@]}
	else 
		sendto=${all_recipients}
		slack_url=${slack_urls[@]}
	fi
elif [[ $group == "matched group2" ]]; then
	if [[ $severity != "Disaster" ]]; then
		sendto="${unit_2_recipients}"
		slack_url=${slack_urls[@]}
	else 
		sendto=${all_recipients}
		slack_url=${slack_urls[@]}
	fi
elif [[ $group == "matched group3" ]]; then
	if [[ $severity != "Disaster" ]]; then
		sendto="${unit_3_recipients}"
		slack_url=${slack_urls[@]}
	else
		sendto=${all_recipients}
		slack_url=${slack_urls[@]}
	fi
fi

# Define the color based on trigger severity
if [[ $type == "P" ]]; then
	if [[ $severity == "Warning" ]] || [[ $severity == 'Average' ]]; then
    	color=${colors[2]}
	elif [[ $severity == "High" ]]; then
		color=${colors[4]}
	elif [[ $severity == "Disaster" ]]; then
		color=${colors[5]};
	elif [[ $severity == "Information" ]]; then
		color=${colors[1]}
	fi
elif [[ $type == "R" ]]; then
		color=${colors[6]}
fi


# Compose payload for slack hook
# Send payload
payload="payload={
        \"channel\": \"${channel}\",
        \"username\": \"${username}\",
		\"text\": \"${sendto}\",
        \"attachments\": [
        	{   
				\"color\": \"${color}\",
				\"blocks\": [
   					{
						\"type\": \"section\",
						\"text\": {
						\"type\": \"mrkdwn\",
						\"text\": \"*<${link}|${title}>*\"
						}
					},
					{
							\"type\": \"section\",
							\"fields\": [
									{
											\"type\": \"mrkdwn\",
											\"text\": \"*Host*\n${server}\"
									},
									{
											\"type\": \"mrkdwn\",
											\"text\": \"*Event time*\n${time}\"
									}
							]
					},
					{
							\"type\": \"section\",
							\"fields\": [
									{
											\"type\": \"mrkdwn\",
											\"text\": \"*Severity*\n${severity}\"
									},
									{
											\"type\": \"mrkdwn\",
											\"text\": \"*Opdata*\n${op_data}\"
									}
							]
					}
        ]
}
        ] }"
if [[ -z "$slack_url"]]; then
	echo "Condition is FALSE no URL detected"
else
	/usr/bin/curl -k -m 5 --data-urlencode "${payload}" $slack_url # Change the path of curl if the curl path doesn't existed
fi
echo $message >> /tmp/message.log # Print the message to a file for debugging 

