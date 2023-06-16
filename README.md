# weewx-notify
Extension for causing weewx to notify a server as it runs

This has been designed as a ping to a monitoring service, with the responsibility of the monitoring service being to
notify the user (e.g. send an e-mail) if the weewx applicaiton has crashed and thus not sent a ping in a pre-determined
amount of time.

This was built for use with the [healthchecks.io](https://healthchecks.io/) monitoring service, but is extensible to 
any service that simply needs a http/https call for a checkin.

## Installing

Download the latest release from the [github releases](https://github.com/teeks99/weewx-notify/releases) page

Run `wee_extension --install=weewx-notify_X.X.tar.gz`

This will automatically add a `[[Notify]]` to your weewx.conf in the `[StdRESTful]` section. Here a unique URL will be 
needed for the service to operate correctly. 

## Uninstalling

Run `wee_extension --uninstall=weewx-notify`