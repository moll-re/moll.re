## Setps:

* Copy `httpd.conf` to `/etc/apache2/conf-enabled/`
* Restart apache2 through systemctl


In order for the config to work additionally:
* `chown` the project folder to www-data
* setup the VE at `project-folder/VE`