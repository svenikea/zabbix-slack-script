#! /usr/bin/python

import logging, sys, re, json, socket
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime

# Slack Alert information
## Slack user/channel ID with different recipient here!
recipients = {
    'unit1'     : [],
    'unit2'     : [],
    'unit3'     : [],
    'unit4'     : [],
    'all_units' : "<!channel>"
}
## Message template
message_template = {
    'channel_id'        : sys.argv[1],
    'subject'           : sys.argv[2],
    'message'           : sys.argv[3],
    'sendto'            : None,
    'response_channel'  : [],
    'color'             : ["#97AAB3", "#7499FF", "#FFC859", "#FFA059", "#E97659", "#E45959", "#009900"],
    'match_groups'      : ["matched group1", "matched group2", "matched group3", "matched group4"]
}
#channel_id, subject, message, sendto, response_channel = sys.argv[1], sys.argv[2], sys.argv[3], None, []
slack_token = "TOKEN" # <= Put the token here

# Function Declaration
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def get_info(argv1):
    return message_template['message'].replace(",", "*").split("*")[argv1] # <= Replace any separator from (,) to (*) or choose what ever separator you want

def send_notification(color, link, title, server, severity, op_data, slack_token ):
    client = WebClient(token=slack_token)
    logger = logging.getLogger(__name__)
    formatted_time  = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    attachment_json = [
        {
            "fallback": "Upgrade your Slack client to use messages like these.",
            "color": color,
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
            channel = message_template['channel_id'], 
            text = message_template['sendto'],
            attachments = attachment_json
        )
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")

# This is the order of the message 0,1,2,3,4,5,6 
# Rember you can change the order the the message just make sure the below variable matched the corresponding order you have changed
server      = get_info(0)
severity    = get_info(1)
op_data     = get_info(2)
event_id    = get_info(3)
status      = get_info(4)
trigger_id  = get_info(5)
group       = get_info(6)
link        = f"http://{get_ip_address()}/zabbix/tr_events.php?triggerid={trigger_id}&eventid={event_id}" #<= In live production http should be change to https

# Set alet message type
if status == "PROBLEM":
    title = f":red_circle: Problem: {message_template['subject']}"
    if severity == "Warning" or severity == "Average":
        selected_color = message_template['color'][2]
    elif severity == "High":
        selected_color = message_template['color'][4]
    elif severity == "Disaster":
        selected_color = message_template['color'][5]
    elif severity == "Information":
        selected_color = message_template['color'][1]
else:
    title = f":large_green_circle: Resolved: {message_template['subject']}"
    selected_color = message_template['color'][6]

#Define alert recipient
if group == message_template['match_groups'][0]:
    if severity != "Disaster":
        channel_id = message_template['response_channel'][0]
        message_template['sendto'] = " ".join(recipients['unit1']) # <= convert a list of unit recipients to string
    else:
        channel_id = message_template['response_channel'][0]
        message_template['sendto'] = recipients['all_units']
elif group ==message_template['match_groups'][1]:
    if severity != "Disaster":
        channel_id = message_template['response_channel'][1]
        message_template['sendto'] = " ".join(recipients['unit2'])
    else:
        channel_id = message_template['response_channel'][1]
        message_template['sendto'] = recipients['all_units']
elif group == message_template['match_groups'][2]:
    if severity != "Disaster":
        channel_id = message_template['response_channel'][2]
        message_template['sendto'] = " ".join(recipients['unit3'])
    else:
        channel_id = message_template['response_channel'][2]
        message_template['sendto'] = recipients['all_units']
elif group == message_template['match_groups'][3]:
    if severity != "Disaster":
        channel_id = message_template['response_channel'][3]
        message_template['sendto'] = " ".join(recipients['unit4'])
    else:
        channel_id = message_template['response_channel'][3]
        message_template['sendto'] = recipients['all_units']

send_notification(selected_color, link, title, server, severity, op_data, slack_token)
print("Debug")
print(channel_id)
print(message_template['sendto'])