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


#
# Database access
#
class DBConnection(object):
    local = 'perfevents-result-collector.conf'
    defaults = 'defaults.conf'
    logger = logging.getLogger()

    def __init__(self, rw=True, use_localhost=False, dryrun=False, debug=False):
        """
        Open new connection to RESULT db.

        @param rw: by default read-only connection is opened, set to True if you need write access
        @param use_localhost: set to True if you intent to connect to db running on localhost
        """
        local_path = os.path.expanduser(os.path.join('~', '.config', self.local))
        if (os.path.isfile(local_path)):
            db_config = local_path
        else:
            db_config = os.path.join(PROJECT_PATH, self.defaults)

        self.dryrun = dryrun
        self.debug = debug

        self.conn = None

        stream_handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        config = ConfigParser.ConfigParser()
        with open(db_config) as fd:
            config.readfp(fd)

        conn_options = {
            'dbname': config.get('Defaults', 'RESULTDB_NAME'),
            'user': config.get('Defaults', 'RESULTDB_USER_RO_NAME'),
            'password': config.get('Defaults', 'RESULTDB_USER_RO_PASSWORD'),
            'host': config.get('Defaults', 'RESULTDB_HOST')
        }

        if use_localhost:
            conn_options['host'] = 'localhost'

        if rw:
            conn_options['user'] = config.get('Defaults', 'RESULTDB_USER_RW_NAME')
            conn_options['password'] = config.get('Defaults', 'RESULTDB_USER_RW_PASSWORD')

        self.conn = psycopg2.connect(
            'dbname={dbname} user={user} password={password} host={host}'.format(**conn_options))

    def close(self):
        if self.conn is None:
            return

        self.conn.close()
        self.conn = None

    def die(self, exc=None):
        if exc is not None:
            self.logger.error(
                'RESULTDB: An error appeared when communicating with the RESULTDB:\nError: %s' % str(exc.pgerror))

        raise SystemExit(1)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def query(self, sql_query, sql_params=None, fetchall=False, dryrun=None, debug=None, on_sql_exception=None):
        """
        Execute SQL query.

        This function should handle all we need from SQL queries - log query and its
        params, log returned values, log SQL errors and exit script in case of failed
        queries. It also honors dry run settings if necessary.

        psycopg2.Error exception is handled - exception is logged, and script quits.

        Returns return value of cursor.fetchall().

        @param db: db connection - e.g. return value of connect() method.
        @param sql_query: SQL query.
        @param sql_params: dict or tuple with params for query.
        @param dryrun: when True, no queries are send to db server. Queries are only
          logged if requested by setting debug param. When None, value passed to
          DBConnection is used.
        @param debug: when True, queries, results, timing, etc. are logged. When None,
          value passed to DBConnection is used.
        """

        assert self.conn is not None

        if dryrun is None:
            dryrun = self.dryrun

        if debug is None:
            debug = self.debug

        if debug:
            import pprint
            import time

        if debug:
            self.logger.debug('RESULTDB: SQL query template: %s' % sql_query)
            self.logger.debug('RESULTDB: SQL params: %s' % pprint.pformat(sql_params))

        cur = self.conn.cursor(cursor_factory=CursorFactory)

        if sql_params:
            sql_query = cur.mogrify(sql_query, sql_params)

        else:
            sql_query = cur.mogrify(sql_query)

        if debug:
            self.logger.debug('RESULTDB: SQL query: %s' % sql_query)

        if dryrun:
            self.logger.info('RESULTDB: SQL dryrun mode enabled, quiting')
            return []

        if debug:
            time_start = time.time()

        cur.execute(sql_query)

        if debug:
            time_query = time.time()

        if fetchall:
            result = cur.fetchall()
        else:
            result = self.conn.commit()

        if debug:
            time_end = time.time()

            self.logger.info('RESULTDB: query result:')
            if fetchall:
                self.logger.info('%s' % pprint.pformat(result))

            self.logger.info('RESULTDB: query took %.4f sec, fetching results took %.4f sec' % (
                time_query - time_start, time_end - time_query))

        return result

    def select(self, *args, **kwargs):
        kwargs['fetchall'] = True
        return self.query(*args, **kwargs)

    def commit(self):
        try:
            self.conn.commit()

        except psycopg2.Error as e:
            self.logger.error(
                'RESULTDB: An error appeared when communicating with the RESULTDB during COMMIT:\n%s' % str(e.pgerror))
            sys.exit(1)


if __name__ == '__main__':
    print("This is a module.")
