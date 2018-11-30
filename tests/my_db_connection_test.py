from _datetime import datetime
import pymysql
import pytest
from src.my_db import MyDB

YEAR = datetime.now().year
OTHER_YEAR = datetime.now().year + 2
DB_NAME = 'home_budget'
OTHER_DB_NAME = 'other_db'
TABLE_NAME = 'budget'
OTHER_TABLE_NAME = 'other_table'


def test_connect_to_my_db():
    """
    Is there already defined database?
    """
    a = MyDB()
    a.connect_to_my_db( db = DB_NAME )
    assert isinstance( a.connection, pymysql.connections.Connection)
    a.close_connection_to_my_db(DB_NAME )
    del a


@pytest.mark.xfail(raises=pymysql.err.OperationalError)
def test_connect_to_db_on_nonexisting_host( ):
    a = MyDB()
    a.connect_to_my_db( host = "some_garbage" )


@pytest.mark.xfail(raises=pymysql.err.OperationalError)
def test_connect_my_db_with_wrong_user( ):
    a = MyDB()
    a.connect_to_my_db( user='some_garbage' )


@pytest.mark.xfail(raises=pymysql.err.OperationalError)
def test_connect_my_db_with_wrong_password( ):
    a = MyDB()
    a.connect_to_my_db( password ='some_garbage' )


@pytest.mark.xfail(raises=pymysql.err.InternalError)
def test_connect_to_nonexisting_db( ):
    a = MyDB()
    a.connect_to_my_db( db = "some_garbage" )
