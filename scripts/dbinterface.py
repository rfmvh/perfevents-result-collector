#!/bin/python

import optparse
import os
import sys
import psycopg2


RESULTDB_HOST = '<IP>'
RESULTDB_NAME = '<dbname>'
RESULTDB_USER_RW = ('readwrite', 'passwd1')
RESULTDB_USER_RO = ('readonly', 'passwd2')

try:
  from psycopg2.extras import DictCursor as CursorFactory
except ImportError:
  CursorFactory = None

#
# Database access
#
class DBConnection(object):
  def __init__(self, rw = True, use_localhost = False, dryrun = False, debug = False):
    """
    Open new connection to RESULT db.

    @param rw: by default read-only connection is opened, set to True if you need write access
    @param use_localhost: set to True if you intent to connect to db running on localhost
    """

    self.dryrun = dryrun
    self.debug = debug

    self.conn = None

    conn_options = {
        'dbname':   RESULTDB_NAME,
        'user':     RESULTDB_USER_RO[0],
        'password': RESULTDB_USER_RO[1],
        'host':     RESULTDB_HOST
    }

    if use_localhost:
      conn_options['host'] = 'localhost'

    if rw:
      conn_options['user'] = RESULTDB_USER_RW[0]
      conn_options['password'] = RESULTDB_USER_RW[1]

    try:
      self.conn = psycopg2.connect('dbname={dbname} user={user} password={password} host={host}'.format(**conn_options))

    except psycopg2.DatabaseError as e:
      print "Error opening DB connection"
      print 'dbname={dbname} user={user} password={password} host={host}'.format(**conn_options)
      raise e

  def close(self):
    if self.conn is None:
      return

    self.conn.close()
    self.conn = None

  def die(self, exc = None):
    if exc is not None:
      sys.stderr.write('RESULTDB: An error appeared when communicating with the RESULTDB:\nError: %s\n' % str(exc.pgerror))

    raise SystemExit(1)

  def __enter__(self):
    return self

  def __exit__(self, *args):
    self.close()

  def query(self, sql_query, sql_params = None, fetchall = False, dryrun = None, debug = None, on_sql_exception = None):
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
      sys.stderr.write('RESULTDB: SQL query template: %s\n' % sql_query)
      sys.stderr.write('RESULTDB: SQL params: %s\n' % pprint.pformat(sql_params))

    try:
      cur = self.conn.cursor(cursor_factory = CursorFactory)

      if sql_params:
        sql_query = cur.mogrify(sql_query, sql_params)

      else:
        sql_query = cur.mogrify(sql_query)

      if debug:
        sys.stderr.write('RESULTDB: SQL query: %s\n' % sql_query)

      if dryrun:
        sys.stderr.write('RESULTDB: SQL dryrun mode enabled, quiting\n')
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

        sys.stderr.write('RESULTDB: query result:\n')
        if fetchall:
          sys.stderr.write('%s\n' % pprint.pformat(result))

        sys.stderr.write('RESULTDB: query took %.4f sec, fetching results took %.4f sec\n' % (time_query - time_start, time_end - time_query))

      return result

    except psycopg2.Error as e:
      self.conn.rollback()

      if on_sql_exception is None:
        self.die(exc = e)

      result = on_sql_exception(self, sql_query, sql_params, e, dryrun = dryrun, debug = debug)
      if result is False:
        self.die(exc = e)

      return result

  def select(self, *args, **kwargs):
    kwargs['fetchall'] = True
    return self.query(*args, **kwargs)

  def commit(self):
    try:
      self.conn.commit()

    except psycopg2.Error as e:
      sys.stderr.write('RESULTDB: An error appeared when communicating with the RESULTDB during COMMIT:\n%s\n' % str(e.pgerror))
      sys.exit(1)

if __name__ == '__main__':
  print("This is a module.")


