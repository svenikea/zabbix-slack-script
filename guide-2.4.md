# Quick-start

Copy ```slack_script.sh``` to ```/usr/lib/zabbix/alertscripts```. This depends on your Zabbix Server Configuration, the configuration usually can be found at ```/etc/zabbix/zabbix_server.conf```

Change the Slack webhook URL at the beginning of the script to match your slack webhook URL. If you don't have one already yet, checkout this [URL](https://api.slack.com/incoming-webhooks).

> The webhook looks like this 
https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX

## Create New Media Type

Go to your Zabbix server and follow this step to create media type: 
```Administration``` -> ```Media types``` -> ```Create media type```

Enter the field then click ```Update```
![new media](./images/zabbix-2.4_create_media.png)

## Create New Action

Go to your Zabbix server and follow this step to create action:
```Configuration``` -> ```Actions``` -> ```Trigger actions``` -> ```Create action```

You can either enter the default subject and message then click ```Add``` or just leave it empty, and use the custom message from the ```operations``` tab

![new action](./images/zabbbix-2.4_create_action.png)

![new operations](./images/zabbix-2.4_create_operations.png)

> The type of subject and message determine the behavior of the script for example this script works with this subject template 

```
Host>{HOST.NAME}>Severity>{TRIGGER.SEVERITY}>opdata>{ITEM.VALUE1}>eventid>{EVENT.ID}>status>{TRIGGER.STATUS}>triggerid>{TRIGGER.ID}>group>{TRIGGER.HOSTGROUP.NAME}
```

> This section of the script will extract the Operating Data from the subject above. It will print the matching string ```opdata``` and some text after that. Then we use the ```cut``` command to remove the ```>``` and select the field #6 which is the data, and finally assign it to a variable named ```op_data```

```
op_data=$(echo ${message} | grep "opdata" | cut -d ">" -f6)
```

## Create new user group 

Go to your Zabbix server and filling the necessary information for new user group:
```Administration``` -> ```Users``` -> ```User group``` -> ```Permissions``` -> ```Update```

![add media](./images/zabbix-2.4_create_usergroup.png)
![add permissions](./images/zabbix-2.4_create_permissions.png)

## Example

> The message will look like this 

![example](./images/example.png)
