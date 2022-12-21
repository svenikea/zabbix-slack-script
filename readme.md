# Zabbix Slack notifications

Simple scripts to send alert notifications to slack from Zabbix. The scripts support python and shell script with different way of sending notification to slack

# Quick-start
Slack support many access methods, this method have different way of sending message to Slack. For example, Slack have dedicated access method for Python, Java and JavaScript through supported module, but outside these are not supported and have to use HTTP method such as a shell script

## HTTP Method
Shell script use HTTP method to send message to Slack via ```Incoming Webhook``` with the ```POST``` method 
* For Zabbix [2.4](./guide-2.4.md) 
* For Zabbix [5.4](./guide-5.4.md)

## Dedicated Post Method

Slack support dedicated ```chat.postMessage``` for languages such as ```JavaScript```, ```Python``` and ```Java```. Checkout this Python [Guide](./python-guide.md)

## Creating Rich Message Layouts

Structure complex data in an easily readable and understandable way within messages. You can learn more about it at their official [document](https://api.slack.com/messaging/composing/layouts)

## Variable Type

|Data       |Usage      |Example|
|-----------|-----------|--------|
|`all_unit`   |To mention all user in a channel| `<!channel>`|
|`unit1_recipients` `unit2_recipients` `unit3_recipients` `unit4_recipients` |A list of users |`["<@U03TGH3MLKN>"], ["<@U03TGH3MLKN>", "<@NBMSVRM1RQX>"]`
|`sendto` |To mention specific user or a list of users| `None`|
|`channel_id` |Initial channel ID to send from Zabbix side |`#general`|
|`subject` |The subject or the title of the alert | Mysql Server is Down |
|`message` |The body of  the alert | EC2,Warning,30,7872822,PROBLEM,876688,group4 |
|`response_channel` |The Target channel id of which the script will send to | `#general` |

## Example

![screenshot](./images/general_screenshot.png)