#! /bin/bash
mysql --defaults-extra-file=/run/init/creds.conf delphi < /run/init/load_data.sql