# Quick Start

Copy ```slack_script.sh``` to ```/usr/lib/zabbix/alertscripts```. This depends on your Zabbix Server Configuration, the configuration usually can be found at ```/etc/zabbix/zabbix_server.conf```

Change the Slack webhook URL at the beginning of the script to match your slack webhook URL. If you don't have one already yet, checkout this [URL](https://api.slack.com/incoming-webhooks).

> The webhook looks like this 
https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX

## Create New Media Type

Go to your Zabbix server and follow this step to create media type: 
```Administration``` -> ```Media types``` -> ```Create media type```

Enter the field then click ```Add```
![new media](./images/new-media.png)

## Create New Action

Go to your Zabbix server and follow this step to create action:
```Configuration``` -> ```Actions``` -> ```Trigger actions``` -> ```Create action```

Enter the field for ```Action``` and ```Operations``` then click ```Add```
![new action](./images/new-action.png)
![new operations](./images/new-operations.png)

## Add New Media to Admin

Go to your Zabbix server and follow this step to add media to admin:
```Administration``` -> ```Users``` -> ```Admin``` -> ```Media``` -> ```Add```

![add media](./images/add-media-to-user.png)

## Example

> The message will look like this 

![example](./images/example.png)
