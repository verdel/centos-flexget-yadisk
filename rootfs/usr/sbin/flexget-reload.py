#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests import Session
import argparse
import sys
import urllib3
import logging


def init_log():
    consolelog_level = logging.INFO

    logger = logging.getLogger('flexget-yadisk')
    logger.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    consolelog = logging.StreamHandler()
    consolelog.setLevel(consolelog_level)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(u'%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')
    # filelog.setFormatter(formatter)
    consolelog.setFormatter(formatter)

    # add the handlers to logger
    logger.addHandler(consolelog)
    # logger.addHandler(filelog)

    return logger


class Flexget(object):
    def __init__(self, url, username, password):
        urllib3.disable_warnings()
        self.url = url
        self.session = Session()
        self.session.verify = False

        response = self.session.post(url='{}/{}'.format(url.strip('/'),
                                                        '/api/auth/login/?remeber=true'),
                                     json={'username': username, 'password': password},
                                     headers={'Accept': 'application/json', 'Content-Type': 'application/json'})

        if response.status_code != 200:
            raise Exception

    def reload(self):
        try:
            response = self.session.post(url='{}/{}'.format(self.url.strip('/'),
                                                            'api/server/manage/'),
                                         json={'operation': 'reload', 'force': True},
                                         headers={'Accept': 'application/json', 'Content-Type': 'application/json'})
        except:
            return False

        if response.status_code == 200:
            return True
        else:
            return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True, help="Flexget API URL")
    parser.add_argument('--username', required=True, help="Flexget API username")
    parser.add_argument('--password', required=True, help="Flexget API password")
    args = parser.parse_args()

    logger = init_log()

    try:
        flexget = Flexget(args.url, args.username, args.password)
    except Exception as e:
        logger.info('Config reload error. {}'.format(e))
        sys.exit(1)

    reload_status = flexget.reload()
    if reload_status:
        logger.info('Config successfully reloaded from disk')
        sys.exit()
    else:
        logger.info('Config reload error')
        sys.exit(1)
