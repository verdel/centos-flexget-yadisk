#!/usr/bin/with-contenv bash

rm $FLEXGET_CONF_DIR/*.yml
cp -rf $FLEXGET_SYNC_DIR/*.yml $FLEXGET_CONF_DIR
/usr/sbin/flexget-reload.py --url $FLEXGET_URL --username $FLEXGET_USERNAME --password $FLEXGET_PASSWORD
