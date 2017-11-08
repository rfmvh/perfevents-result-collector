#!/usr/bin/env python

import optparse
import os
import sys
import psycopg2
import ConfigParser
import logging

try:
    from psycopg2.extras import DictCursor as CursorFactory
except ImportError:
    CursorFactory = None

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

LOGGER = logging.getLogger()


class DBConnection(object):
    def __init__(self, dryrun=False):
        self.dryrun = dryrun
        self.conn = None
        self.db_connect()

    def get_user_parms(self):
        local = 'perfevents-result-collector.conf'
        defaults = 'defaults.conf'
        local_path = os.path.expanduser(os.path.join('~', '.config', local))

        if (os.path.isfile(local_path)):
            db_config = local_path
        else:
            db_config = os.path.join(PROJECT_PATH, defaults)

        config = ConfigParser.ConfigParser()
        with open(db_config) as fd:
            config.readfp(fd)
        return {
            'dbname': config.get('Defaults', 'RESULTDB_NAME'),
            'user': config.get('Defaults', 'RESULTDB_USER_RO_NAME'),
            'password': config.get('Defaults', 'RESULTDB_USER_RO_PASSWORD'),
            'host': config.get('Defaults', 'RESULTDB_HOST')}

    def db_connect(self):
        self.conn = psycopg2.connect(
            'dbname={dbname} user={user} password={password} host={host}'.format(**self.get_user_parms()))

    def select(self, query, parms=None):
        if parms == None:
            parms = []
        if self.dryrun:
            LOGGER.info('RESULTDB: SQL dryrun mode enabled, quiting')
            return []
        cur = self.conn.cursor()
        sql_quert = cur.mogrify(query, parms)
        cur.execute(sql_quert)
        result = cur.fetchall()
        cur.close()

        return result

    def db_close(self):
        if self.conn is None:
            return

        self.conn.close()
        self.conn = None
