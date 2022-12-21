#! /usr/bin/python3

import logging, sys, re, json, socket
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime

# Slack Alert information
## Slack user/channel ID with different recipient here!
unit1_recipients, unit2_recipients, unit3_recipients, unit4_recipients, all_unit = [], [], [], [], "<!channel>"
## Message template
channel_id, subject, message, sendto, response_channel = sys.argv[1], sys.argv[2], sys.argv[3], None, []

# Function Declaration
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def get_info(argv1):
    return message.replace(",", "*").split("*")[argv1]
    
server=get_info(0)
severity=get_info(1)
op_data=get_info(2)
event_id=get_info(3)
status=get_info(4)
trigger_id=get_info(5)
group=get_info(6)
formatted_time=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
colors=["#97AAB3", "#7499FF", "#FFC859", "#FFA059", "#E97659", "#E45959", "#009900"]
link=f"http://{get_ip_address()}/zabbix/tr_events.php?triggerid={trigger_id}&eventid={event_id}"

# Set alet message type
if status == "PROBLEM":
    title=f":red_circle: Problem: {subject}"
    if severity == "Warning" or severity == "Average":
        selected_color=colors[2]
    elif severity == "High":
        selected_color=colors[4]
    elif severity == "Disaster":
        selected_color=colors[5]
    elif severity == "Information":
        selected_color=colors[1]
else:
    title=f":large_green_circle: Resolved: {subject}"
    selected_color=colors[6]

#Define alert recipient
if group == "matched group1":
    if severity != "Disaster":
        channel_id=response_channel[0]
        sendto=" ".join(unit1_recipients)
    else:
        channel_id=response_channel[0]
        sendto=all_unit
elif group == "matched group2":
    if severity != "Disaster":
        channel_id=response_channel[1]
        sendto=" ".join(unit2_recipients)
    else:
        channel_id=response_channel[1]
        sendto=all_unit
elif group == "matched group3":
    if severity != "Disaster":
        channel_id=response_channel[2]
        sendto=" ".join(unit3_recipients)
    else:
        channel_id=response_channel[2]
        sendto=all_unit
elif group == "matched group4":
    if severity != "Disaster":
        channel_id=response_channel[3]
        sendto=" ".join(unit4_recipients)
    else:
        channel_id=response_channel[3]
        sendto=all_unit
        
client = WebClient(token=("TOKEN_HERE"))
logger = logging.getLogger(__name__)
attachment_json= [
    {
        "fallback": "Upgrade your Slack client to use messages like these.",
        "color": selected_color,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*<{link}|{title}>*"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Host*\n{server}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Event time*\n{formatted_time}"
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Serverity*\n{severity}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*OpData*\n{op_data}"
                    }
                ]
            }
        ]
    }
]
try:
    # Call the chat.postMessage method using the WebClient
    result = client.chat_postMessage(
        channel=channel_id, 
        text=sendto,
        attachments=attachment_json
    )
    logger.info(result)

except SlackApiError as e:
    logger.error(f"Error posting message: {e}")